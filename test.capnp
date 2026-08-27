
@0x934efea7f017fff0;
struct ModelBundle { 
    status @0 :DownloadStatus; 
    enum DownloadStatus { notDownloading @0; downloading @1; downloaded @2; failed @3; }
}
