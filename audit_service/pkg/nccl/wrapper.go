package nccl

/*
#cgo LDFLAGS: -lnccl -lcudart
#include <nccl.h>
#include <cuda_runtime.h>
#include <stdlib.h>

int get_version() {
    int version;
    ncclResult_t res = ncclGetVersion(&version);
    if (res != ncclSuccess) {
        return -1;
    }
    return version;
}
*/
import "C"
import (
	"errors"
	"fmt"
)

func GetNCCLVersion() (string, error) {
	ver := C.get_version()
	if int(ver) == -1 {
		return "", errors.New("falha ao carregar a biblioteca NCCL da NVIDIA")
	}
	return fmt.Sprintf("NCCL Version: %d", int(ver)), nil
}
