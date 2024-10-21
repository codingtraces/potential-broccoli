Here’s a step-by-step guide based on the Spring Initializr screenshot you’ve shared. This guide will walk you through setting up the Spring Boot project with the required dependencies to handle XML to JSON conversion using both file upload and raw XML input.

Step 1: Open Spring Initializr

You can use either:

	1.	Spring Initializr web interface: https://start.spring.io
	2.	IntelliJ IDEA: It comes with built-in Spring Initializr support.

Step 2: Configure Project Metadata

On the Spring Initializr page (as shown in the screenshot):

	1.	Project:
	•	Select Maven or Gradle based on preference.
(We’ll proceed with Maven here).
	2.	Language:
	•	Select Java.
	3.	Spring Boot Version:
	•	Select 3.3.4 (as shown in your screenshot).
	4.	Project Metadata:
	•	Group: com.jackson
	•	Artifact: xmltojson
	•	Name: xmltojson
	•	Package Name: com.jackson.xmltojson
	•	Description: XML to JSON conversion API for Jackson Insurance.
	5.	Packaging:
	•	Select JAR.
	6.	Java Version:
	•	Select 17 (LTS version recommended).

Step 3: Add Dependencies

Click on the “Add Dependencies” button. Add the following dependencies:

	1.	Spring Web: To create REST endpoints.
	2.	Jackson Dataformat XML: To convert XML to JSON.

Step 4: Generate the Project

	1.	Click the “Generate” button.
A ZIP file will be downloaded with your Spring Boot project.
	2.	Unzip the project to a folder on your machine.
	3.	Open IntelliJ IDEA.
	4.	Import the Project:
	•	Go to File > Open.
	•	Select the unzipped project folder.

Step 5: Update the Project Structure

Ensure that the following folders are present inside your project:

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

Step 6: Implement the Code

1. Main Application Class – XmlToJsonApplication.java

package com.jackson.xmltojson;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class XmlToJsonApplication {
    public static void main(String[] args) {
        SpringApplication.run(XmlToJsonApplication.class, args);
    }
}

2. XML to JSON Converter – XmlJsonConverter.java

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

    // Handle raw XML input
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

    // Handle XML file upload
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

Step 7: Run the Application

	1.	Build the project in IntelliJ:
	•	Go to Build > Build Project or press Ctrl + F9.
	2.	Run the application:
	•	Right-click on XmlToJsonApplication and select Run ‘XmlToJsonApplication’.
The application will start on http://localhost:8080.

Step 8: Test the API

Using Postman

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

Response:

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

Uploading an XML File via Postman

	1.	Method: POST
	2.	URL: http://localhost:8080/api/xmltojson/upload
	3.	Headers:
	•	Content-Type: multipart/form-data
	4.	Body:
	•	Select form-data and add:
	•	Key: file (type: File)
	•	Upload an XML file (e.g., policy.xml).

Step 9: Summary

This version provides:

	1.	Raw XML input handling via a REST endpoint.
	2.	File upload support for XML conversion.
	3.	Modular design for easy future enhancements.

This solution gives you flexibility to:

	•	Expand with data enrichment or rules-based customization.
	•	Add support for cloud integration or asynchronous processing in the future.

Let me know if you have any further questions or need help!