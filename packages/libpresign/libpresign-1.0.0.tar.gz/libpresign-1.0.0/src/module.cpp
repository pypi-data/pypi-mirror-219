#include "module.h"


extern "C" {
    static PyObject *
    get(PyObject *self, PyObject *args, PyObject *kwargs) {
        char *access_key_id;
        char *secret_access_key;
        char *region;
        char *bucket;
        char *key;
        unsigned int expires = 3600;

        static char *kwlist[] = {(char*)"access_key_id", (char*)"secret_access_key", (char*)"region", (char*)"bucket", (char*)"key", (char*)"expires",  NULL};

        if (!PyArg_ParseTupleAndKeywords(args, kwargs, "sszss|I:libpresign.get", kwlist, &access_key_id, &secret_access_key, &region, &bucket, &key, &expires)) {
            printf("error");
            return PyUnicode_FromString("None");
        }

        if (region == NULL) { // in case region is passed as None
            region = (char*) "us-east-1";
        }

        return PyUnicode_FromString(generatePresignedURL(access_key_id, secret_access_key, region, bucket, key, expires).c_str());
    }
}