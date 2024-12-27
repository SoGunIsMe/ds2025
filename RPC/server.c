#include "RPC/file_transfer.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int* upload_file_1_svc(FileData* file_data, struct svc_req* req) {
    static int result;
    static FILE* file = NULL;

    if (!file) {
        file = fopen(file_data->filename, "wb");
        if (!file) {
            perror("Failed to create file");
            result = -1;
            return &result;
        }
    }

    fwrite(file_data->content.content_val, 1, file_data->content.content_len, file);

    if (file_data->is_last_chunk) {
        fclose(file);
        file = NULL;
        printf("File received successfully: %s\n", file_data->filename);
    }

    result = 0;
    return &result;
}
