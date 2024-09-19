Sure! Let’s create a Java program that correctly parses a FAP-like file and generates a Word document while maintaining correct font sizes, paragraph formatting, and other properties.

### Step 1: Understanding the Font Size Issue

The issue with extremely large font sizes likely stems from incorrect scaling or interpreting the FAP font size inappropriately. We'll set up a more logical scaling approach, assuming the FAP file uses reasonable font size units (e.g., `12` for 12pt font size).

### Step 2: Code Implementation

Here’s the full code without image handling, focusing on generating properly formatted paragraphs with correct font sizes:

#### 1. `pom.xml`

Ensure you have the correct dependencies in your `pom.xml`:

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

#### 2. `FapParser.java`

This class handles parsing the FAP file, extracting text content, font size, and style:

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
            }
        }

        return elements;
    }

    private FapElement parseTextElement(String line) {
        String[] parts = line.split(",", 7); // Split into 7 parts
        String content = parts[6].trim(); // The text content
        String fontDetails = parts[3]; // Font details and positioning
        int fontSize = Integer.parseInt(parts[4].trim()); // Extract the font size

        return new FapElement("TEXT", content, fontDetails, fontSize);
    }

    public static class FapElement {
        private final String type;
        private final String content;
        private final String fontDetails;
        private final int fontSize;

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

#### 3. `WordGenerator.java`

This class generates the Word document, handling text with proper formatting:

```java
package org.example;

import org.apache.poi.xwpf.usermodel.ParagraphAlignment;
import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.apache.poi.xwpf.usermodel.XWPFParagraph;
import org.apache.poi.xwpf.usermodel.XWPFRun;

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
        // Assuming FAP font size directly correlates to points for simplicity
        return fapFontSize; // No unnecessary conversion
    }

    private void setFontStyle(XWPFRun run, String fontDetails) {
        if (fontDetails != null && fontDetails.contains("Bold")) {
            run.setBold(true);
        }
        if (fontDetails != null && fontDetails.contains("Italic")) {
            run.setItalic(true);
        }
        // Additional styles can be added as needed
    }
}
```

#### 4. `Main.java`

The main class ties everything together:

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

### Step 3: Sample `sample.fap` File

Place this content in your `input/sample.fap` file:

```plaintext
H,2400,(0,0),(0,0,26400,20400),SampleLetterFAP
V,"A123456X","JOHN","Mon Jan 01 10:00:00 2022",".","."
V,"B654321X","DOE","Mon Jan 01 10:15:00 2022",".","."
M,TT,(18952,4460,19296,5364),(20011,Bold,14),1,Dear John Doe,
M,TT,(18952,5386,19296,6418),(20011,Regular,12),2,We are pleased to inform you that your application has been approved.
M,TT,(18952,6440,19296,6940),(20011,Regular,12),3,Please find the details below regarding your approval and next steps.
M,TT,(18952,7500,19296,8000),(20011,Regular,12),4,Your contract will commence on February 1, 2022.
M,TT,(18952,8500,19296,9000),(20011,Regular,12),5,If you have any questions, please contact our support team.
M,TT,(18952,9500,19296,10000),(20011,Bold,14),6,Thank you,
M,TT,(18952,10500,19296,11000),(20011,Bold,14),7,Your Company Name
M,E
```

### Step 4: Run the Application

1. **Build the Project**:
   - In IntelliJ IDEA, go to **Build > Build Project**.

2. **Run the Application**:
   - Run `Main.java` as a Java application.

3. **Check the Output**:
   - A new `sample.docx` should be generated in the `output` directory. Open it to verify that it contains properly formatted paragraphs with correct font sizes.

### Expected Output

- **Paragraphs**: The document should have paragraphs formatted according to the FAP file.
- **Font Sizes**: Text should be displayed with the appropriate font sizes, like `14pt` for headers and `12pt` for body text.
- **Styles**: Bold and italic styles should be applied correctly where specified.

### Troubleshooting

- **Font Size Issues**: If you notice incorrect font sizes, double-check that the FAP file uses reasonable sizes and that the `getFontSize()` method interprets them correctly.
- **Missing Text**: Ensure the FAP parsing correctly captures all content. The parsing logic should be adapted if your FAP structure changes.

This solution should address the issues with font sizes and provide a consistent, properly formatted Word document output.
