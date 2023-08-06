#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "libgrav.h"
// #include <pthread.h>

#define PY_SSIZE_T_CLEAN
#include "Python.h"


#define NUM_THREADS 1
#define MAX_RF 100000


// Vector3 type
typedef struct Vector3 {
    double x;
    double y;
    double z;
} Vector3;

void * failure(PyObject *type, const char *message) {
    PyErr_SetString(type, message);
    return NULL;
}

void * success(PyObject *var){
    Py_INCREF(var);
    return var;
}

double req;
double mu;
int model_index;
int body_index;
Vector3 rfs[MAX_RF];
Vector3 gs[MAX_RF];

double Vector3Norm(Vector3 v) {
    return sqrt(v.x*v.x + v.y*v.y + v.z*v.z);
}

Vector3 Vector3Scale(Vector3 v, double s) {
    return (Vector3) {v.x*s, v.y*s, v.z*s};
}

Vector3 Vector3Hat(Vector3 v) {
    return Vector3Scale(v, 1.0/Vector3Norm(v));
}

enum BODY {
    EARTH,
    MOON,
    MARS,
};

enum MODEL {
    EGM96,
    GRGM360, // https://pds-geosciences.wustl.edu/grail/grail-l-lgrs-5-rdr-v1/grail_1001/shbdr/gggrx_1200a_shb_l180.lbl
    MRO120F, // https://pds-geosciences.wustl.edu/mro/mro-m-rss-5-sdp-v1/mrors_1xxx/data/shadr/jgmro_120f_sha.lbl
};

void set_indices(char* model_name, int *model_index, int *body_index) {
    if(strcmp(model_name, "EGM96") == 0) { // if they're the same
        *body_index = EARTH;
        *model_index = EGM96;
    }
    else if(strcmp(model_name, "GRGM360") == 0) {
        *body_index = MOON;
        *model_index = GRGM360;
    }
    else if(strcmp(model_name, "MRO120F") == 0) {
        *body_index = MARS;
        *model_index = MRO120F;
    }
}


void set_body_params(int body_index, double *mu, double *req) {
    if(body_index == EARTH) {
        *mu = 398600.44;
        *req = 6378.137;
    }
    if(body_index == MOON) {
        *mu = 4902.8001224453001;
        *req = 1738.0;
    }
    if(body_index == MARS) {
        *mu = 42828.3748574;
        *req = 3396.0;
    }
}


int nm2i(int n, int m) {
    return n * (n+1) / 2 + m;
}

void read_cnm_snm(int nmax, int model_index, double cnm[], double snm[]) {
    // printf("Starting coefficients read!\n");
    int num = ncoef_EGM96 + 100;
    const int* n = (int*) malloc(ncoef_EGM96 * sizeof(int));
    const int* m = (int*) malloc(ncoef_EGM96 * sizeof(int));
    const double* c = (double*) malloc(ncoef_EGM96 * sizeof(double));
    const double* s = (double*) malloc(ncoef_EGM96 * sizeof(double));

    if(model_index == EGM96) {
        // Coefficients from: https://raw.githubusercontent.com/lukasbystricky/SpaceSimulator/master/Environment/Geopoential/coefficients/egm96_to360.ascii
        n = n_EGM96; 
        m = m_EGM96; 
        c = c_EGM96; 
        s = s_EGM96; 
        num = ncoef_EGM96;
    }
    if(model_index == GRGM360) {
        n = n_GRGM360; 
        m = m_GRGM360; 
        c = c_GRGM360; 
        s = s_GRGM360; 
        num = ncoef_GRGM360;
        // Coefficients from: https://pds-geosciences.wustl.edu/grail/grail-l-lgrs-5-rdr-v1/grail_1001/shadr/gggrx_1200a_sha.tab
    }
    if(model_index == MRO120F) {
        n = n_MRO120F; 
        m = m_MRO120F; 
        c = c_MRO120F; 
        s = s_MRO120F; 
        num = ncoef_MRO120F;
        // Coefficients from: https://pds-geosciences.wustl.edu/mro/mro-m-rss-5-sdp-v1/mrors_1xxx/data/shadr/jgmro_120f_sha.tab
    }
    
    int i;
    for(i = 0; i < num; i++) {
        int ind = nm2i(*(n+i), *(m+i));
        cnm[ind] = *(c+i);
        snm[ind] = *(s+i);
        // printf("n=%d, m=%d, c=%.2e, s=%.2e, cnm=%.2e, snm=%.2e\n", *(n+i), *(m+i), *(c+i), *(s+i), cnm[ind], snm[ind]);
        if(*(m+i) == nmax) {
            break;
        }
    }

    snm[0] = 0.0;
    cnm[0] = 1.0;
    // printf("Finished coefficients read!\n");
    return;
}

Vector3 pinesnorm(Vector3 rf, double cnm[],
               double snm[], int nmax, double mu, double req) {
    // printf("Starting pinesnorm!\n");   
    // Based on pinesnorm() from: https://core.ac.uk/download/pdf/76424485.pdf
    double rmag = Vector3Norm(rf);
    Vector3 stu = Vector3Hat(rf);
    int anm_sz = nm2i(nmax+3, nmax+3);
    double *anm = malloc(anm_sz * sizeof(double)); //ansi-c
    anm[0] = sqrt(2.0);

    int m;
    for(m = 0; m <= nmax+2; m++) {
        if(m != 0) { // DIAGONAL RECURSION
            anm[nm2i(m,m)] = sqrt(1.0+1.0/(2.0*m))*anm[nm2i(m-1,m-1)];
        }
        if(m != nmax+2) { // FIRST OFF-DIAGONAL RECURSION 
            anm[nm2i(m+1,m)] = sqrt(2*m+3)*stu.z*anm[nm2i(m,m)];
        }
        if(m < nmax+1) {
            int n;
            for(n = m+2; n <= nmax+2; n++) {
                double alpha_num = (2*n+1)*(2*n-1);
                double alpha_den = (n-m)*(n+m);
                double alpha = sqrt(alpha_num/alpha_den);
                double beta_num = (2*n+1)*(n-m-1)*(n+m-1);
                double beta_den = (2*n-3)*(n+m)*(n-m);
                double beta = sqrt(beta_num/beta_den);
                anm[nm2i(n,m)] = alpha*stu.z*anm[nm2i(n-1,m)] - beta*anm[nm2i(n-2,m)];
            }
        }
    }
    int n;
    for(n = 0; n <= nmax+2; n++) {
        anm[nm2i(n,0)] *= sqrt(0.50);
    }
     
    double* rm = (double*) malloc((nmax+2) * sizeof(double)); //ansi-c
    double* im = (double*) malloc((nmax+2) * sizeof(double)); //ansi-c
    rm[0] = 0.00; rm[1] = 1.00; 
    im[0] = 0.00; im[1] = 0.00; 
    for(m = 2; m < nmax+2; m++) {
        rm[m] = stu.x*rm[m-1] - stu.y*im[m-1]; 
        im[m] = stu.x*im[m-1] + stu.y*rm[m-1];
    }
    double rho  = mu/(req*rmag);
    double rhop = req/rmag;
    double g1 = 0.00; double g2 = 0.00; double g3 = 0.00; double g4 = 0.00;
    for(n = 0; n <= nmax; n++) {
        double g1t = 0.0; double g2t = 0.0; double g3t = 0.0; double g4t = 0.0;
        double sm = 0.5;
        int m;
        for(m = 0; m <= n; m++) {
            double anmp1;
            if(n == m) {
                anmp1 = 0.0;
            }
            else {
                anmp1 = anm[nm2i(n,m+1)];
            }

            double dnm = cnm[nm2i(n,m)]*rm[m+1] + snm[nm2i(n,m)]*im[m+1];
            double enm = cnm[nm2i(n,m)]*rm[m] + snm[nm2i(n,m)]*im[m];
            double fnm = snm[nm2i(n,m)]*rm[m] - cnm[nm2i(n,m)]*im[m];
            double alpha  = sqrt(sm*(n-m)*(n+m+1));
            g1t += anm[nm2i(n,m)]*m*enm;
            g2t += anm[nm2i(n,m)]*m*fnm;
            g3t += alpha*anmp1*dnm;
            g4t += ((n+m+1)*anm[nm2i(n,m)]+alpha*stu.z*anmp1)*dnm;
            // printf("ANM: %d %d %.2e %.2e\n", n, m, anm[nm2i(n,m)], anmp1);
            // printf("DEF: %d %d %.2e %.2e %.2e\n", n, m, dnm, enm, fnm);
            // printf("G1-4t: %d %d %.2e %.2e %.2e %.2e\n", n, m, g1t, g2t, g3t, g4t);
            // printf("CS: %d %d %.2e %.2e\n", n, m, cnm[nm2i(n,m)], snm[nm2i(n,m)]);
            if(m == 0) sm = 1.0;
        }
        rho *= rhop;
        g1 += rho*g1t; 
        g2 += rho*g2t; 
        g3 += rho*g3t; 
        g4 += rho*g4t;
        // printf("n=%d, g1 = %.2e, g2 = %.2e, g3 = %.2e, g4 = %.2e\n", 
        // n, g1, g2, g3, g4);
    }
    Vector3 rv = (Vector3) {g1-g4*stu.x, g2-g4*stu.y, g3-g4*stu.z};

    free(anm);

    return rv;
}

typedef struct thread_args{
    int start_ind;
    int end_ind;
    int nmax;
    double *cnm;
    double *snm;
}thread_args;

void* thread_func(void* arg) {
    struct thread_args *targs = (struct thread_args *)arg;
    int i;
    for(i = targs->start_ind; i < targs->end_ind; i++) {
        gs[i] = pinesnorm(rfs[i], targs->cnm, targs->snm, targs->nmax, mu, req);
    }
    return NULL;
}

static PyObject *egm96_gravity(PyObject *self, PyObject *args) {
    PyObject *r_ecef;
    int nmax;
    char* model_name = NULL;
    if (!PyArg_ParseTuple(args, "Ois", 
                            &r_ecef, 
                            &nmax,
                            &model_name))
        return failure(PyExc_RuntimeError, "Failed to parse parameters.");
    
    int npts = PyObject_Length(r_ecef) / 3;
    double* x = (double*) malloc(npts * sizeof(double)); //ansi-c
    double* y = (double*) malloc(npts * sizeof(double));
    double* z = (double*) malloc(npts * sizeof(double));

    int i;
    for (i = 0; i < npts; i++) {
        x[i] = PyFloat_AsDouble((PyObject*) PyList_GetItem(r_ecef, 3*i));
        y[i] = PyFloat_AsDouble((PyObject*) PyList_GetItem(r_ecef, 3*i+1));
        z[i] = PyFloat_AsDouble((PyObject*) PyList_GetItem(r_ecef, 3*i+2));
    }

    set_indices(model_name, &model_index, &body_index);
    set_body_params(body_index, &mu, &req);
    int sz = nm2i(nmax+2, nmax+2);
    double* cnm = (double*) malloc(sz * sizeof(double)); //ansi-c
    double* snm = (double*) malloc(sz * sizeof(double));
    read_cnm_snm(nmax, model_index, cnm, snm);

    for(i = 0; i < npts; i++) {
        rfs[i] = (Vector3){x[i], y[i], z[i]};
    }

    // pthread_t thread[NUM_THREADS];
    // pthread_attr_t attr;
    // pthread_attr_init(&attr);
    // size_t stacksize;
    // pthread_attr_getstacksize(&attr, &stacksize);
    // pthread_attr_setstacksize(&attr, 2*stacksize);

    // thread_args targs[NUM_THREADS];

    // for(int i = 0; i < NUM_THREADS; i++) {
    //     int start_ind = i * npts / NUM_THREADS;
    //     int end_ind = (i+1) * npts / NUM_THREADS;
    //     targs[i] = (thread_args) {start_ind, end_ind, nmax, &cnm, &snm};
    // }

    // for(int i = 0; i < NUM_THREADS; i++) {
    //     pthread_create(&thread[i], &attr, &thread_func, &targs[i]);
    // }
    // for(int i = 0; i < NUM_THREADS; i++) {
    //     if (pthread_join(thread[i], NULL) != 0) {
    //         printf("ERROR : pthread join failed.\n");
    //         return (0);
    //     }
    // }

    // If we just want to run on one thread
    thread_func(&(thread_args) {0, npts, nmax, cnm, snm});
    
    PyObject* accel_vector = PyList_New(3 * npts);
    double* res = (double*) malloc(3 * npts * sizeof(double));
    for(i = 0; i < npts; i++) {
        res[3*i + 0] = gs[i].x;
        res[3*i + 1] = gs[i].y;
        res[3*i + 2] = gs[i].z;
        
        PyList_SetItem(accel_vector, 3*i+0, PyFloat_FromDouble(gs[i].x));
        PyList_SetItem(accel_vector, 3*i+1, PyFloat_FromDouble(gs[i].y));
        PyList_SetItem(accel_vector, 3*i+2, PyFloat_FromDouble(gs[i].z));
    }
    return accel_vector;
}

static PyMethodDef acceleration_method[] = {
    {"_grav", /* The name as a C string. */
    egm96_gravity,   /* The C function to invoke. */
    METH_VARARGS, 
    "Computes the body-fixed acceleration vector at a body-fixed position",
    }
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "_grav",
    "Python interface to the gravitas C functions",
    -1, // the size of the module’s global state
    acceleration_method
};

PyMODINIT_FUNC PyInit__grav(void) {
    return PyModule_Create(&module);
}
