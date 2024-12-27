program FILE_TRANSFER_PROG {
    version FILE_TRANSFER_VERS {
        int upload_file(FileData) = 1;
    } = 1;
} = 0x23451111;

struct FileData {
    string filename<256>;
    opaque content<1024>;
    bool is_last_chunk;
};