#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <filesystem>
#include <tinyxml2.h>
#include <ctime>

class XmlFileHandler {
public:
    XmlFileHandler(const std::string& logFileName) {
        logFile.open(logFileName, std::ios::out | std::ios::app);
        if (!logFile.is_open()) {
            throw std::runtime_error("无法打开日志文件");
        }
    }

    ~XmlFileHandler() {
        if (logFile.is_open()) {
            logFile.close();
        }
    }

    std::vector<std::pair<std::string, std::string>> readXmlFilesFromDirectory(const std::string& directory) {
        std::vector<std::pair<std::string, std::string>> xmlData;

        for (const auto& entry : std::filesystem::directory_iterator(directory)) {
            if (entry.path().extension() == ".xml") {
                std::string filePath = entry.path().string();
                tinyxml2::XMLDocument doc;
                tinyxml2::XMLError eResult = doc.LoadFile(filePath.c_str());
                
                if (eResult == tinyxml2::XML_SUCCESS) {
                    xmlData.push_back({entry.path().filename().string(), doc.Print()});
                    logInfo("成功读取 XML 文件: " + filePath);
                } else {
                    logError("解析 XML 文件出错: " + filePath + ", 错误: " + std::to_string(eResult));
                }
            }
        }
        return xmlData;
    }

    void writeXmlToDirectory(const std::vector<std::pair<std::string, std::string>>& xmlData, const std::string& directory) {
        if (!std::filesystem::exists(directory)) {
            std::filesystem::create_directories(directory);
        }

        for (const auto& [fileName, xmlContent] : xmlData) {
            std::string filePath = directory + "/" + fileName;
            std::ofstream ofs(filePath);
            if (ofs) {
                ofs << xmlContent;
                logInfo("成功写入 XML 到文件: " + filePath);
            } else {
                logError("写入 XML 文件出错: " + filePath);
            }
        }
    }

private:
    std::ofstream logFile;

    void logInfo(const std::string& message) {
        log("INFO", message);
    }

    void logError(const std::string& message) {
        log("ERROR", message);
    }

    void log(const std::string& level, const std::string& message) {
        std::time_t now = std::time(nullptr);
        logFile << std::asctime(std::localtime(&now)) << " - " << level << " - " << message << std::endl;
    }
};

int main() {
    try {
        std::string sourceDir = "path_to_source_directory"; // 替换为你的源XML文件目录
        std::string targetDir = "path_to_target_directory"; // 替换为你的目标目录，用于写入XML文件
        XmlFileHandler xmlHandler("operation.log");

        auto xmlData = xmlHandler.readXmlFilesFromDirectory(sourceDir);
        xmlHandler.writeXmlToDirectory(xmlData, targetDir);

    } catch (const std::exception& e) {
        std::cerr << "发生错误: " << e.what() << std::endl;
    }

    return 0;
}
