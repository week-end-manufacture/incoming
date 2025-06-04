#include "imglib.h"


int print_imglib()
{
    printf("IMGLIB\n");

    return 0;
}

int remove_all_exif_data(src_path, dst_path)
const char *src_path;
const char *dst_path;
{
    FILE *src = fopen(src_path, "rb");
    if (!src) return -1;

    FILE *dst = fopen(dst_path, "wb");

    if (!dst)
    {
        fclose(src);
        return -1;
    }

    unsigned char marker[2];
    // SOI(0xFFD8) 복사
    if (fread(marker, 1, 2, src) != 2 || marker[0] != 0xFF || marker[1] != 0xD8)
    {
        fclose(src);
        fclose(dst);
        return -1;
    }

    fwrite(marker, 1, 2, dst);

    // 세그먼트 순회
    while (fread(marker, 1, 2, src) == 2)
    {
        if (marker[0] != 0xFF) break;

        // SOS(0xDA) 이후는 이미지 데이터이므로 모두 복사
        if (marker[1] == 0xDA)
        {
            fwrite(marker, 1, 2, dst);
            int c;
            while ((c = fgetc(src)) != EOF) fputc(c, dst);
            break;
        }

        // 세그먼트 길이 읽기
        unsigned char len_bytes[2];
        if (fread(len_bytes, 1, 2, src) != 2) break;

        unsigned short seg_len = (len_bytes[0] << 8) | len_bytes[1];

        // EXIF(0xE1) 세그먼트는 건너뜀
        if (marker[1] == 0xE1)
        {
            fseek(src, seg_len - 2, SEEK_CUR);
            continue;
        }

        // 그 외 세그먼트는 복사
        fwrite(marker, 1, 2, dst);
        fwrite(len_bytes, 1, 2, dst);

        unsigned char *buf = malloc(seg_len - 2);

        if (!buf) break;

        if (fread(buf, 1, seg_len - 2, src) != seg_len - 2)
        {
            free(buf);
            break;
        }

        fwrite(buf, 1, seg_len - 2, dst);
        free(buf);
    }

    fclose(src);
    fclose(dst);

    return 0;
}

int get_image_size(filename, width, height)
const char *filename;
int *width;
int *height;
{
    FILE *fp = fopen(filename, "rb");
    if (!fp) return -1;

    unsigned char header[24];
    if (fread(header, 1, 24, fp) != 24)
    {
        fclose(fp);
        return -1;
    }

    // JPEG
    if (header[0] == 0xFF && header[1] == 0xD8)
    {
        int i = 2;
        while (i < 24)
        {
            if (header[i] == 0xFF && header[i + 1] == 0xC0)
            {
                *height = (header[i + 5] << 8) | header[i + 6];
                *width = (header[i + 7] << 8) | header[i + 8];
                fclose(fp);
                return 0;
            }
            i += (header[i + 2] << 8) | header[i + 3] + 2;
        }
    }
    // PNG
    else if (header[0] == 0x89 && header[1] == 'P' && header[2] == 'N' && header[3] == 'G')
    {
        *width = (header[16] << 24) | (header[17] << 16) | (header[18] << 8) | header[19];
        *height = (header[20] << 24) | (header[21] << 16) | (header[22] << 8) | header[23];
        fclose(fp);
        return 0;
    }
    // BMP
    else if (header[0] == 'B' && header[1] == 'M')
    {
        *width = *(int *)&header[18];
        *height = *(int *)&header[22];
        fclose(fp);
        return 0;
    }
    // GIF
    else if (header[0] == 'G' && header[1] == 'I' && header[2] == 'F')
    {
        *width = (header[6] << 8) | header[7];
        *height = (header[8] << 8) | header[9];
        fclose(fp);
        return 0;
    }
    // TIFF
    else if ((header[0] == 0x49 && header[1] == 0x49 && header[2] == 0x2A && header[3] == 0x00) ||
             (header[0] == 0x4D && header[1] == 0x4D && header[2] == 0x00 && header[3] == 0x2A))
    {
        int offset = (header[0] == 0x49) ? 8 : 4;
        *width = *(int *)&header[offset + 18];
        *height = *(int *)&header[offset + 22];
        fclose(fp);
        return 0;
    }
    // WebP
    else if (header[0] == 'R' && header[1] == 'I' && header[2] == 'F' && header[3] == 'F' &&
             header[8] == 'W' && header[9] == 'E' && header[10] == 'B' && header[11] == 'P')
    {
        *width = (header[12] << 24) | (header[13] << 16) | (header[14] << 8) | header[15];
        *height = (header[16] << 24) | (header[17] << 16) | (header[18] << 8) | header[19];
        fclose(fp);
        return 0;
    }

    fclose(fp);

    return -1; // Unsupported format
}