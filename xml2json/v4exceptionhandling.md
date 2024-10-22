To make your XML to JSON conversion application **robust and professional**, we will add **comprehensive exception handling**. This ensures that the API can:

1. Handle different types of exceptions gracefully.
2. Provide **detailed error messages** and **consistent HTTP status codes**.
3. Log exceptions using a standard logging framework such as **SLF4J**.
4. Follow **industry standards** with a **global exception handler** for centralized error management.

Below is the **improved code** with enhanced exception handling.

---

## **1. Add Dependencies for Logging**

In your `pom.xml`, add the **SLF4J and Logback** dependencies for logging:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-logging</artifactId>
</dependency>
```

Logback is included by default with Spring Boot. This ensures **all exceptions are logged** effectively.

---

## **2. Define Custom Exception Classes**

These classes represent specific exceptions that your application can encounter.

### **FileProcessingException.java**

```java
package com.infosys.xmltojson.exception;

public class FileProcessingException extends RuntimeException {
    public FileProcessingException(String message) {
        super(message);
    }

    public FileProcessingException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

### **XmlParsingException.java**

```java
package com.infosys.xmltojson.exception;

public class XmlParsingException extends RuntimeException {
    public XmlParsingException(String message) {
        super(message);
    }

    public XmlParsingException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

---

## **3. Global Exception Handler**

This **centralized exception handler** ensures that all exceptions are handled consistently.

### **GlobalExceptionHandler.java**

```java
package com.infosys.xmltojson.exception;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.multipart.MaxUploadSizeExceededException;

import java.util.HashMap;
import java.util.Map;

@ControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    // Handle XML Parsing Errors
    @ExceptionHandler(XmlParsingException.class)
    public ResponseEntity<Map<String, String>> handleXmlParsingException(XmlParsingException ex) {
        logger.error("XML Parsing Error: {}", ex.getMessage());
        Map<String, String> response = new HashMap<>();
        response.put("error", "Invalid XML Format");
        response.put("message", ex.getMessage());
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(response);
    }

    // Handle File Upload Errors
    @ExceptionHandler(FileProcessingException.class)
    public ResponseEntity<Map<String, String>> handleFileProcessingException(FileProcessingException ex) {
        logger.error("File Processing Error: {}", ex.getMessage());
        Map<String, String> response = new HashMap<>();
        response.put("error", "File Processing Failed");
        response.put("message", ex.getMessage());
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
    }

    // Handle File Size Limits
    @ExceptionHandler(MaxUploadSizeExceededException.class)
    public ResponseEntity<Map<String, String>> handleMaxSizeException(MaxUploadSizeExceededException ex) {
        logger.error("File size exceeds the limit.");
        Map<String, String> response = new HashMap<>();
        response.put("error", "File size too large");
        response.put("message", "Please upload a smaller file.");
        return ResponseEntity.status(HttpStatus.PAYLOAD_TOO_LARGE).body(response);
    }

    // Handle Generic Errors
    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, String>> handleGenericException(Exception ex) {
        logger.error("Unexpected Error: {}", ex.getMessage());
        Map<String, String> response = new HashMap<>();
        response.put("error", "Internal Server Error");
        response.put("message", "An unexpected error occurred. Please try again later.");
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
    }
}
```

---

## **4. Integrate Exception Handling in Controller**

Update the controller to **throw exceptions** when necessary.

### **XmlToJsonController.java**

```java
package com.infosys.xmltojson.controller;

import com.fasterxml.jackson.databind.JsonNode;
import com.infosys.xmltojson.exception.FileProcessingException;
import com.infosys.xmltojson.exception.XmlParsingException;
import com.infosys.xmltojson.util.XmlJsonConverter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@RestController
@RequestMapping("/api/xmltojson")
public class XmlToJsonController {

    private static final Logger logger = LoggerFactory.getLogger(XmlToJsonController.class);

    @Autowired
    private XmlJsonConverter xmlJsonConverter;

    @PostMapping(path = "/raw", consumes = MediaType.APPLICATION_XML_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<JsonNode> convertXmlToJsonRaw(@RequestBody String xmlContent) {
        try {
            JsonNode jsonResponse = xmlJsonConverter.convertXmlToJson(xmlContent);
            return ResponseEntity.ok(jsonResponse);
        } catch (IOException e) {
            logger.error("Error parsing XML: {}", e.getMessage());
            throw new XmlParsingException("Failed to parse XML", e);
        }
    }

    @PostMapping(path = "/upload", consumes = MediaType.MULTIPART_FORM_DATA_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<JsonNode> convertXmlToJsonFile(@RequestParam("file") MultipartFile file) {
        try {
            String xmlContent = new String(file.getBytes());
            JsonNode jsonResponse = xmlJsonConverter.convertXmlToJson(xmlContent);
            return ResponseEntity.ok(jsonResponse);
        } catch (IOException e) {
            logger.error("Error processing file: {}", e.getMessage());
            throw new FileProcessingException("Failed to process uploaded file", e);
        }
    }

    @PostMapping(path = "/splitRaw", consumes = MediaType.APPLICATION_XML_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<List<JsonNode>> splitRawXmlByRecipient(@RequestBody String xmlContent) {
        try {
            List<JsonNode> recipientJsonList = xmlJsonConverter.splitXmlByRecipients(xmlContent);
            return ResponseEntity.ok(recipientJsonList);
        } catch (IOException e) {
            logger.error("Error parsing XML: {}", e.getMessage());
            throw new XmlParsingException("Failed to parse XML", e);
        }
    }

    @PostMapping(path = "/manipulate", consumes = MediaType.APPLICATION_XML_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<JsonNode> manipulateXmlToJson(@RequestBody String xmlContent, @RequestParam String condition) {
        try {
            JsonNode jsonResponse = xmlJsonConverter.manipulateAndConvert(xmlContent, condition);
            return ResponseEntity.ok(jsonResponse);
        } catch (IOException e) {
            logger.error("Error manipulating XML: {}", e.getMessage());
            throw new XmlParsingException("Failed to manipulate XML", e);
        }
    }
}
```

---

## **5. Final Improvements and Summary**

### **Key Features:**
- **Exception Handling:**
  - Centralized with a **global exception handler** using `@ControllerAdvice`.
  - Logs errors with **SLF4J** for traceability.
  - Returns consistent **HTTP responses** with meaningful error messages.

- **Resilience:**
  - Handles unexpected XML formats without relying on hardcoded models.
  - Supports **dynamic manipulation** of JSON during conversion.

- **Endpoints Provided:**
  1. **Raw XML to JSON**: `/api/xmltojson/raw`
  2. **Upload XML to JSON**: `/api/xmltojson/upload`
  3. **Split XML by Recipients**: `/api/xmltojson/splitRaw`
  4. **Manipulate XML to JSON**: `/api/xmltojson/manipulate`

---

## **6. Testing the Application**

Use **Postman** or **cURL** to test the endpoints. Try uploading:
- **Valid XML** to ensure smooth conversion.
- **Malformed XML** to see the error handling in action.
- **Large Files** to trigger the file size limit exception.

---

With this implementation, your application is now **production-ready**, equipped with **exception handling, logging, and scalability**. Let me know if you need further adjustments!
