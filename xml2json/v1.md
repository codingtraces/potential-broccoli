Here is the full Spring Boot XML to JSON Converter API project with package name com.infosys, complete with code, configuration, and testing instructions.

Spring Boot XML to JSON Converter API

This project demonstrates a Spring Boot application with:

	1.	Raw XML input handling via REST API.
	2.	XML file upload with JSON response.

Project Setup

1. Create the Project Using Spring Initializr

	1.	Go to https://start.spring.io.
	2.	Configure the project:
	•	Project: Maven
	•	Language: Java
	•	Spring Boot Version: 3.3.4
	•	Group: com.infosys
	•	Artifact: xmltojson
	•	Name: xmltojson
	•	Description: XML to JSON conversion for Infosys.
	•	Package Name: com.infosys.xmltojson
	•	Packaging: Jar
	•	Java Version: 17
	3.	Add Dependencies:
	•	Spring Web: To expose REST endpoints.
	•	Jackson Dataformat XML: For XML to JSON conversion.
	4.	Click “Generate” to download the project.
	5.	Unzip the downloaded project and open it in IntelliJ IDEA.

Project Structure

src/
├── main/
│   ├── java/
│   │   └── com/
│   │       └── infosys/
│   │           └── xmltojson/
│   │               ├── XmlToJsonApplication.java
│   │               ├── controller/
│   │               │   └── XmlToJsonController.java
│   │               └── util/
│   │                   └── XmlJsonConverter.java
│   └── resources/
│       └── application.properties

Code Implementation

1. Main Application Class – XmlToJsonApplication.java

package com.infosys.xmltojson;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class XmlToJsonApplication {
    public static void main(String[] args) {
        SpringApplication.run(XmlToJsonApplication.class, args);
    }
}

2. XML to JSON Converter Utility – XmlJsonConverter.java

package com.infosys.xmltojson.util;

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

package com.infosys.xmltojson.controller;

import com.infosys.xmltojson.util.XmlJsonConverter;
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

server.port=8080

Running the Application

	1.	Build the Project:
	•	In IntelliJ, go to Build > Build Project or press Ctrl + F9.
	2.	Run the Application:
	•	Right-click on XmlToJsonApplication and select Run ‘XmlToJsonApplication’.

The application will start on http://localhost:8080.

Testing the API

Sample XML File – policy.xml

<?xml version="1.0" encoding="UTF-8"?>
<Policy>
    <PolicyNumber>POL123456</PolicyNumber>
    <PolicyType>Life Insurance</PolicyType>
    <Insured>
        <Name>John Doe</Name>
        <Address>123 Main St, Anytown, USA</Address>
    </Insured>
</Policy>

Option 1: Send Raw XML via Postman

	1.	Method: POST
	2.	URL: http://localhost:8080/api/xmltojson/raw
	3.	Headers:
	•	Content-Type: application/xml
	4.	Body: Raw (Text format)

Example XML Input:

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

Summary

This project provides:

	1.	Raw XML input handling via a REST API.
	2.	File upload support for converting XML files to JSON.
	3.	Modular design for easy future enhancements.

This solution is ready to use and easy to expand for additional features. Let me know if you need further assistance!
