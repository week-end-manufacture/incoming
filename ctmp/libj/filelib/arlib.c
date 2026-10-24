#include "arlib.h"


int print_arlib()
{
    printf("ARLIB\n");

    return 0;
}

static int zip_file_list(zip_path, filelist, filecount)
const char *zip_path;
char filelist[][1024];
int *filecount;
{
    FILE *fp = fopen(zip_path, "rb");
    if (!fp) return -1;

    unsigned char buf[4];
    int count = 0;

    while (fread(buf, 1, 4, fp) == 4)
    {
        // Local file header signature: 0x04034b50
        if (buf[0] == 0x50 && buf[1] == 0x4b && buf[2] == 0x03 && buf[3] == 0x04)
        {
            fseek(fp, 22, SEEK_CUR); // skip to filename length
            unsigned short fname_len, extra_len;
            fread(&fname_len, 2, 1, fp);
            fread(&extra_len, 2, 1, fp);

            if (fname_len > 0 && fname_len < 256 && count < 256)
            {
                fread(filelist[count], 1, fname_len, fp);
                filelist[count][fname_len] = '\0';
                count++;
            }
            else
            {
                fseek(fp, fname_len, SEEK_CUR);
            }

            fseek(fp, extra_len, SEEK_CUR);
        }
        else
        {
            // 다음 바이트로 이동
            fseek(fp, -3, SEEK_CUR);
        }
    }

    fclose(fp);
    *filecount = count;

    return 0;
}

static int rar_file_list(rar_path, filelist, filecount)
const char *rar_path;
char filelist[][1024];
int *filecount;
{
    FILE *fp = fopen(rar_path, "rb");
    if (!fp) return -1;

    unsigned char buf[7];
    int count = 0;

    while (fread(buf, 1, 7, fp) == 7)
    {
        // RAR file header signature: 0x52617221
        if (buf[0] == 0x52 && buf[1] == 0x61 && buf[2] == 0x72 && buf[3] == 0x21)
        {
            fseek(fp, 4, SEEK_CUR); // skip to filename length
            unsigned short fname_len;
            fread(&fname_len, 2, 1, fp);

            if (fname_len > 0 && fname_len < 256 && count < 256)
            {
                fread(filelist[count], 1, fname_len, fp);
                filelist[count][fname_len] = '\0';
                count++;
            }
            else
            {
                fseek(fp, fname_len, SEEK_CUR);
            }
        }
        else
        {
            // 다음 바이트로 이동
            fseek(fp, -6, SEEK_CUR);
        }
    }

    fclose(fp);
    *filecount = count;

    return 0;
}

static int seven_zip_file_list(seven_zip_path, filelist, filecount)
const char *seven_zip_path;
char filelist[][1024];
int *filecount;
{
    FILE *fp = fopen(seven_zip_path, "rb");
    if (!fp) return -1;

    unsigned char buf[6];
    int count = 0;

    while (fread(buf, 1, 6, fp) == 6)
    {
        // 7-Zip file header signature: 0x377abcaf
        if (buf[0] == 0x37 && buf[1] == 0x7a && buf[2] == 0xbc && buf[3] == 0xaf)
        {
            fseek(fp, 26, SEEK_CUR); // skip to filename length
            unsigned short fname_len;
            fread(&fname_len, 2, 1, fp);

            if (fname_len > 0 && fname_len < 256 && count < 256)
            {
                fread(filelist[count], 1, fname_len, fp);
                filelist[count][fname_len] = '\0';
                count++;
            }
            else
            {
                fseek(fp, fname_len, SEEK_CUR);
            }
        }
        else
        {
            // 다음 바이트로 이동
            fseek(fp, -5, SEEK_CUR);
        }
    }

    fclose(fp);
    *filecount = count;

    return 0;
}

int get_compressed_file_list(const char *archive_path, char filelist[][1024], int *filecount)
{
    if (strstr(archive_path, ".zip") != NULL)
    {
        return zip_file_list(archive_path, filelist, filecount);
    }
    else if (strstr(archive_path, ".rar") != NULL)
    {
        return rar_file_list(archive_path, filelist, filecount);
    }
    else if (strstr(archive_path, ".7z") != NULL)
    {
        return seven_zip_file_list(archive_path, filelist, filecount);
    }
    
    return -1; // Unsupported archive format
}