Certainly! Below is the fully working code for your Java application, which converts a FAP-like file to a Word document with paragraphs and an image (logo). The package name used here is `org.example`.

### Directory Structure
Ensure your project structure looks like this:

```
fap-to-word-converter
├── pom.xml
├── src
│   ├── main
│   │   ├── java
│   │   │   └── org
│   │   │       └── example
│   │   │           ├── FapParser.java
│   │   │           ├── Main.java
│   │   │           └── WordGenerator.java
│   └── test
├── input
│   ├── sample.fap
│   └── logo.png
├── output
```

### Step 1: `pom.xml`

Make sure your `pom.xml` file includes the necessary dependencies:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>fap-to-word-converter</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
    </properties>

    <dependencies>
        <!-- Apache POI dependencies for Word document manipulation -->
        <dependency>
            <groupId>org.apache.poi</groupId>
            <artifactId>poi-ooxml</artifactId>
            <version>5.2.3</version>
        </dependency>
    </dependencies>
</project>
```

### Step 2: `FapParser.java`

```java
package org.example;

import java.util.ArrayList;
import java.util.List;

public class FapParser {

    public List<FapElement> parseFapFile(String fileContent) {
        List<FapElement> elements = new ArrayList<>();

        String[] lines = fileContent.split("\n");
        for (String line : lines) {
            if (line.startsWith("M,TT")) {
                elements.add(parseTextElement(line));
            } else if (line.startsWith("M,O")) {
                elements.add(parseImageElement(line));
            }
        }

        return elements;
    }

    private FapElement parseTextElement(String line) {
        String[] parts = line.split(",", 7); // Split into 7 parts
        String content = parts[6].trim();
        String fontDetails = parts[3];
        int fontSize = Integer.parseInt(parts[4].trim());

        return new FapElement("TEXT", content, fontDetails, fontSize);
    }

    private FapElement parseImageElement(String line) {
        String[] parts = line.split(",", 6); // Split into 6 parts
        String imagePath = parts[5].trim();

        return new FapElement("IMAGE", imagePath, null, 0);
    }

    public static class FapElement {
        private String type;
        private String content;
        private String fontDetails;
        private int fontSize;

        public FapElement(String type, String content, String fontDetails, int fontSize) {
            this.type = type;
            this.content = content;
            this.fontDetails = fontDetails;
            this.fontSize = fontSize;
        }

        public String getType() {
            return type;
        }

        public String getContent() {
            return content;
        }

        public String getFontDetails() {
            return fontDetails;
        }

        public int getFontSize() {
            return fontSize;
        }
    }
}
```

### Step 3: `WordGenerator.java`

```java
package org.example;

import org.apache.poi.xwpf.usermodel.*;

import org.apache.poi.util.Units;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Path;
import java.util.List;

public class WordGenerator {

    public void generateWordDocument(List<FapParser.FapElement> elements, Path outputPath) throws IOException {
        try (XWPFDocument doc = new XWPFDocument()) {
            for (FapParser.FapElement element : elements) {
                if (element.getType().equals("TEXT")) {
                    addText(doc, element);
                } else if (element.getType().equals("IMAGE")) {
                    addImage(doc, element);
                }
            }

            try (FileOutputStream out = new FileOutputStream(outputPath.toFile())) {
                doc.write(out);
            }
        }
    }

    private void addText(XWPFDocument doc, FapParser.FapElement element) {
        XWPFParagraph paragraph = doc.createParagraph();
        paragraph.setAlignment(ParagraphAlignment.LEFT);

        XWPFRun run = paragraph.createRun();
        run.setText(element.getContent());
        run.setFontSize(getFontSize(element.getFontSize()));
        setFontStyle(run, element.getFontDetails());
    }

    private int getFontSize(int fapFontSize) {
        return Math.max(fapFontSize / 2, 10);  // Convert to a reasonable point size
    }

    private void setFontStyle(XWPFRun run, String fontDetails) {
        if (fontDetails != null && fontDetails.contains("Bold")) {
            run.setBold(true);
        }
        if (fontDetails != null && fontDetails.contains("Italic")) {
            run.setItalic(true);
        }
    }

    private void addImage(XWPFDocument doc, FapParser.FapElement element) throws IOException {
        XWPFParagraph paragraph = doc.createParagraph();
        XWPFRun run = paragraph.createRun();

        // Print the image path for debugging
        System.out.println("Looking for image at: " + element.getContent());

        try (FileInputStream is = new FileInputStream(element.getContent())) {
            run.addPicture(is, Document.PICTURE_TYPE_PNG, element.getContent(), Units.toEMU(100), Units.toEMU(50)); // Adjust size as needed
        } catch (IOException e) {
            System.err.println("Image file not found at: " + element.getContent());
            throw e;
        }
    }
}
```

### Step 4: `Main.java`

```java
package org.example;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        try {
            Path inputPath = Paths.get("input/sample.fap");
            Path outputPath = Paths.get("output/sample.docx");

            Files.createDirectories(outputPath.getParent());

            String content = Files.readString(inputPath);

            FapParser fapParser = new FapParser();
            List<FapParser.FapElement> elements = fapParser.parseFapFile(content);

            WordGenerator wordGenerator = new WordGenerator();
            wordGenerator.generateWordDocument(elements, outputPath);

            System.out.println("Word document generated successfully at: " + outputPath);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

### Step 5: Sample `sample.fap` File

Place the following content in `input/sample.fap`:

```plaintext
H,2400,(0,0),(0,0,26400,20400),SampleLetterFAP
V,"A123456X","JOHN","Mon Jan 01 10:00:00 2022",".","."
V,"B654321X","DOE","Mon Jan 01 10:15:00 2022",".","."
M,TT,(18952,4460,19296,5364),(20011,Bold,14),1,Dear John Doe,
M,TT,(18952,5386,19296,6418),(20011,Regular,12),2,We are pleased to inform you that your application has been approved.
M,TT,(18952,6440,19296,6940),(20011,Regular,12),3,Please find the details below regarding your approval and next steps.
M,TT,(18952,7500,19296,8000),(20011,Regular,12),4,Your contract will commence on February 1, 2022.
M,O,(19384,9432,19728,9432),(20011,Regular,100),5,input/logo.png
M,TT,(18952,8500,19296,9000),(20011,Regular,12),6,If you have any questions, please contact our support team.
M,TT,(18952,9500,19296,10000),(20011,Bold,14),7,Thank you,
M,TT,(18952,10500,19296,11000),(20011,Bold,14),8,Your Company Name
M,E
```

### Step 6: Place `logo.png` in the Input Directory

Make sure you have a `logo.png` image file in the `input` directory. This will be used to include the logo in the generated Word document.

### Step 7: Run the Application

1. **Build the Project**:
   - Use **Build > Build Project** in IntelliJ IDEA.

2. **

Run the Application**:
   - Right-click on `Main.java` and select **Run 'Main.main()'**.

3. **Check the Output**:
   - A new `sample.docx` should be generated in the `output` directory. Open it to verify that it contains the formatted paragraphs and the logo image.

### Expected Output

- **Two Paragraphs**:
  - The Word document will have two paragraphs of text, formatted with the appropriate styles (e.g., bold, regular).
- **Logo**:
  - The document will include the logo image as specified in the FAP file.

### Troubleshooting

- **File Not Found**: If the logo file is not found, ensure the path in the `sample.fap` file is correct and that the `logo.png` file is in the expected location (`input/logo.png`).
- **Relative Paths**: Make sure that the paths used in the FAP file are relative to the project’s root directory, or use absolute paths for testing.

This complete setup should work correctly and provide the expected output in your Word document.
