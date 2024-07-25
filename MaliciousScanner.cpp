#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <filesystem>
#include <stdexcept>
#include <cstdio> // for popen
#include <memory>

class MaliciousScanner {
public:
    MaliciousScanner(const std::string& logFileName) : logFileName(logFileName) {}

    void scanDirectory(const std::string& directory) {
        checkMaliciousFiles(directory);
        checkMaliciousProcesses();
    }

private:
    const std::vector<std::string> maliciousFiles = {"virus.exe", "malware.dll", "trojan.py"};
    std::string logFileName;

    void checkMaliciousFiles(const std::string& directory) {
        std::vector<std::string> detectedFiles;

        for (const auto& entry : std::filesystem::recursive_directory_iterator(directory)) {
            if (entry.is_regular_file()) {
                for (const auto& maliciousFile : maliciousFiles) {
                    if (entry.path().filename() == maliciousFile) {
                        detectedFiles.push_back(entry.path().string());
                    }
                }
            }
        }

        if (!detectedFiles.empty()) {
            raiseExceptionAndLog("Detected malicious files: " + join(detectedFiles, ", "));
        }
    }

    void checkMaliciousProcesses() {
        std::vector<std::string> detectedProcesses;
        std::string command = "ps -e";
        std::array<char, 128> buffer;
        std::string result;

        std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(command.c_str(), "r"), pclose);
        if (!pipe) {
            raiseExceptionAndLog("Failed to run command");
        }

        while (fgets(buffer.data(), buffer.size(), pipe.get())) {
            result += buffer.data();
        }

        // 检查进程，这里只做示例
        std::string maliciousProcess = "malicious_process"; // 替换为实际的恶意进程名
        if (result.find(maliciousProcess) != std::string::npos) {
            detectedProcesses.push_back(maliciousProcess);
        }

        if (!detectedProcesses.empty()) {
            raiseExceptionAndLog("Detected malicious processes: " + join(detectedProcesses, ", "));
        }
    }

    void writeLog(const std::string& message) {
        std::ofstream logfile(logFileName, std::ios::app);
        logfile << message << "\n";
    }

    void raiseExceptionAndLog(const std::string& message) {
        writeLog(message);
        throw std::runtime_error(message);
    }

    std::string join(const std::vector<std::string>& vec, const std::string& delim) {
        std::string result;
        for (const auto& s : vec) {
            if (!result.empty()) {
                result += delim;
            }
            result += s;
        }
        return result;
    }
};

int main() {
    const std::string directory = "/path/to/scan"; // 替换为要扫描的目录
    const std::string logFileName = "scan_log.txt";

    try {
        MaliciousScanner scanner(logFileName);
        scanner.scanDirectory(directory);

        std::cout << "Scan completed successfully. No malicious files or processes found." << std::endl;

    } catch (const std::exception& e) {
        std::cerr << "Error occurred during scan: " << e.what() << std::endl;
    }

    return 0;
}
