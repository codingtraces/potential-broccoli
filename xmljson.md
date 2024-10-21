Below is the detailed implementation of the Spring Boot XML to JSON Converter API, covering both raw XML input and file uploads. This guide will help you step by step, ensuring the code is complete, correct, and ready for deployment.

Step-by-Step Guide

1. Create the Project Using Spring Initializr

	1.	Go to https://start.spring.io.
	2.	Configure the project:
	•	Project: Maven
	•	Language: Java
	•	Spring Boot Version: 3.3.4
	•	Group: com.jackson
	•	Artifact: xmltojson
	•	Name: xmltojson
	•	Description: XML to JSON conversion for Jackson Insurance
	•	Package Name: com.jackson.xmltojson
	•	Packaging: Jar
	•	Java Version: 17
	3.	Add Dependencies:
	•	Spring Web: To expose REST endpoints.
	•	Jackson Dataformat XML: For XML to JSON conversion.
	4.	Click “Generate” to download the project.
	5.	Unzip the downloaded project and open it in IntelliJ IDEA.

2. Project Structure

After following the steps, your project structure will look like this:

src/
├── main/
│   ├── java/
│   │   └── com/
│   │       └── jackson/
│   │           └── xmltojson/
│   │               ├── XmlToJsonApplication.java
│   │               ├── controller/
│   │               │   └── XmlToJsonController.java
│   │               └── util/
│   │                   └── XmlJsonConverter.java
│   └── resources/
│       └── application.properties

3. Code Implementation

1. Main Application Class – XmlToJsonApplication.java

This is the entry point for the Spring Boot application.

package com.jackson.xmltojson;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class XmlToJsonApplication {
    public static void main(String[] args) {
        SpringApplication.run(XmlToJsonApplication.class, args);
    }
}

2. XML to JSON Converter Utility – XmlJsonConverter.java

This class handles the conversion of XML to JSON using Jackson’s XmlMapper.

package com.jackson.xmltojson.util;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.dataformat.xml.XmlMapper;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class XmlJsonConverter {

    private final XmlMapper xmlMapper = new XmlMapper();

    public String convertXmlToJson(String xmlContent) throws IOException {
        JsonNode jsonNode = xmlMapper.readTree(xmlContent);
        return jsonNode.toPrettyString();
    }
}

3. REST Controller – XmlToJsonController.java

This controller exposes two endpoints:

	1.	POST /api/xmltojson/raw: Accepts raw XML input in the request body.
	2.	POST /api/xmltojson/upload: Accepts an XML file upload.

package com.jackson.xmltojson.controller;

import com.jackson.xmltojson.util.XmlJsonConverter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@RestController
@RequestMapping("/api/xmltojson")
public class XmlToJsonController {

    @Autowired
    private XmlJsonConverter xmlJsonConverter;

    /**
     * Converts raw XML input from the request body to JSON.
     */
    @PostMapping(
            path = "/raw",
            consumes = MediaType.APPLICATION_XML_VALUE,
            produces = MediaType.APPLICATION_JSON_VALUE
    )
    public ResponseEntity<String> convertXmlToJsonRaw(@RequestBody String xmlContent) {
        try {
            String jsonResponse = xmlJsonConverter.convertXmlToJson(xmlContent);
            return ResponseEntity.ok(jsonResponse);
        } catch (IOException e) {
            return ResponseEntity.badRequest().body("Error processing XML: " + e.getMessage());
        }
    }

    /**
     * Converts an uploaded XML file to JSON.
     */
    @PostMapping(
            path = "/upload",
            consumes = MediaType.MULTIPART_FORM_DATA_VALUE,
            produces = MediaType.APPLICATION_JSON_VALUE
    )
    public ResponseEntity<String> convertXmlToJsonFile(@RequestParam("file") MultipartFile file) {
        try {
            String xmlContent = new String(file.getBytes());
            String jsonResponse = xmlJsonConverter.convertXmlToJson(xmlContent);
            return ResponseEntity.ok(jsonResponse);
        } catch (IOException e) {
            return ResponseEntity.badRequest().body("Error processing XML file: " + e.getMessage());
        }
    }
}

4. Configuration – application.properties

Since this version is simple, we don’t need specific configurations. Ensure the application.properties file remains empty or add the following:

server.port=8080

5. Running the Application

	1.	Build the Project:
	•	In IntelliJ, go to Build > Build Project or press Ctrl + F9.
	2.	Run the Application:
	•	Right-click on XmlToJsonApplication and select Run ‘XmlToJsonApplication’.

The application will start on http://localhost:8080.

6. Testing the API

Option 1: Send Raw XML via Postman

	1.	Method: POST
	2.	URL: http://localhost:8080/api/xmltojson/raw
	3.	Headers:
	•	Content-Type: application/xml
	4.	Body: Raw (Text format)

Example XML:

<?xml version="1.0" encoding="UTF-8"?>
<Policy>
    <PolicyNumber>POL123456</PolicyNumber>
    <PolicyType>Life Insurance</PolicyType>
    <Insured>
        <Name>John Doe</Name>
        <Address>123 Main St, Anytown, USA</Address>
    </Insured>
</Policy>

Expected JSON Response:

{
  "Policy": {
    "PolicyNumber": "POL123456",
    "PolicyType": "Life Insurance",
    "Insured": {
      "Name": "John Doe",
      "Address": "123 Main St, Anytown, USA"
    }
  }
}

Option 2: Upload XML File via Postman

	1.	Method: POST
	2.	URL: http://localhost:8080/api/xmltojson/upload
	3.	Headers:
	•	Content-Type: multipart/form-data
	4.	Body:
	•	Select form-data.
	•	Add Key: file (type: File).
	•	Upload an XML file (e.g., policy.xml).

Using curl for Testing

Raw XML Input:

curl -X POST http://localhost:8080/api/xmltojson/raw \
-H "Content-Type: application/xml" \
-d '<?xml version="1.0" encoding="UTF-8"?><Policy><PolicyNumber>POL123456</PolicyNumber><PolicyType>Life Insurance</PolicyType><Insured><Name>John Doe</Name><Address>123 Main St, Anytown, USA</Address></Insured></Policy>'

File Upload:

curl -F "file=@/path/to/policy.xml" http://localhost:8080/api/xmltojson/upload

7. Summary

This version provides:

	1.	Raw XML input handling via a REST API.
	2.	File upload support to convert XML files to JSON.
	3.	Easy-to-understand structure with modular design for future enhancements.

This solution gives you flexibility for real-time conversion and file uploads, making it ideal for both internal APIs and client-facing applications.

Let me know if you have further questions or need additional enhancements!