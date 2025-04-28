// Define template presets for common document types
const DOCUMENT_TEMPLATES = {
    aadhar: [
        { name: "Aadhaar Number", pattern: "regex:\\d{4}\\s\\d{4}\\s\\d{4}", type: "regex" },
        { name: "Name", pattern: "name", type: "keyword" },
        { name: "DOB", pattern: "regex:\\d{2}/\\d{2}/\\d{4}", type: "regex" }
    ],
    pan: [
        { name: "PAN Number", pattern: "regex:[A-Z]{5}\\d{4}[A-Z]{1}", type: "regex" },
        { name: "Name", pattern: "name", type: "keyword" }
    ],
    passport: [
        { name: "Passport Number", pattern: "regex:[A-Z]\\d{7}", type: "regex" },
        { name: "Name", pattern: "given name", type: "keyword" },
        { name: "Surname", pattern: "surname", type: "keyword" },
        { name: "Nationality", pattern: "nationality", type: "keyword" }
    ],
    driving: [
        { name: "License Number", pattern: "regex:(?:DL|dl)[-\\s]?\\d{5}[\\s/-]?\\d{5,}", type: "regex" },
        { name: "Name", pattern: "name", type: "keyword" },
        { name: "DOB", pattern: "DOB", type: "keyword" }
    ]
};

// Initialize event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    setupFileUploadPreview();
    setupCustomFieldsToggle();
    setupFieldTemplateButtons();
    setupAddFieldButton();
    setupExtractButton();
    setupDownloadButtons();
});

// Set up file upload and preview functionality
function setupFileUploadPreview() {
    const fileInput = document.getElementById("fileUpload");
    fileInput.addEventListener("change", function() {
        const file = this.files.length > 0 ? this.files[0] : null;
        const fileNameElem = document.getElementById("fileName");
        const filePreview = document.getElementById("filePreview");
        
        if (file) {
            fileNameElem.textContent = file.name;
            // If the file is an image, display a preview
            if (file.type.startsWith("image/")) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    filePreview.src = e.target.result;
                    filePreview.style.display = "block";
                };
                reader.readAsDataURL(file);
            } else {
                filePreview.style.display = "none";
            }
        } else {
            fileNameElem.textContent = "No file chosen";
            filePreview.style.display = "none";
        }
    });
}

// Set up toggle for custom fields section
function setupCustomFieldsToggle() {
    const enableCustomFieldsCheckbox = document.getElementById('enableCustomFields');
    const customFieldsContainer = document.getElementById('customFieldsContainer');
    
    enableCustomFieldsCheckbox.addEventListener('change', function() {
        customFieldsContainer.style.display = this.checked ? 'block' : 'none';
    });
}

// Set up buttons for document templates
function setupFieldTemplateButtons() {
    document.getElementById('aadharTemplate').addEventListener('click', () => loadTemplate('aadhar'));
    document.getElementById('panTemplate').addEventListener('click', () => loadTemplate('pan'));
    document.getElementById('passportTemplate').addEventListener('click', () => loadTemplate('passport'));
    document.getElementById('drivingTemplate').addEventListener('click', () => loadTemplate('driving'));
}

// Load a template of predefined fields
function loadTemplate(templateName) {
    const fieldsList = document.getElementById('fieldsList');
    fieldsList.innerHTML = ''; // Clear existing fields
    
    if (DOCUMENT_TEMPLATES[templateName]) {
        DOCUMENT_TEMPLATES[templateName].forEach(field => {
            addFieldToUI(field.name, field.pattern, field.type);
        });
    }
}

// Set up add field button
function setupAddFieldButton() {
    document.getElementById('addFieldBtn').addEventListener('click', function() {
        addFieldToUI('', '', 'keyword');
    });
}

// Add a new field entry to the UI
function addFieldToUI(name = '', pattern = '', type = 'keyword') {
    const fieldsList = document.getElementById('fieldsList');
    
    const fieldEntry = document.createElement('div');
    fieldEntry.className = 'field-entry';
    
    // Field name input
    const nameInput = document.createElement('input');
    nameInput.type = 'text';
    nameInput.className = 'field-input field-name-input';
    nameInput.placeholder = 'Field name (e.g., Aadhaar Number)';
    nameInput.value = name;
    
    // Field pattern input
    const patternInput = document.createElement('input');
    patternInput.type = 'text';
    patternInput.className = 'field-input field-pattern-input';
    patternInput.placeholder = type === 'keyword' ? 'Keyword (e.g., DOB)' : 'Regex pattern (e.g., \\d{4}\\s\\d{4}\\s\\d{4})';
    patternInput.value = type === 'regex' && pattern.startsWith('regex:') ? pattern.slice(6) : pattern;
    
    // Field type select
    const typeSelect = document.createElement('select');
    typeSelect.className = 'field-type-select';
    
    const keywordOption = document.createElement('option');
    keywordOption.value = 'keyword';
    keywordOption.textContent = 'Keyword';
    
    const regexOption = document.createElement('option');
    regexOption.value = 'regex';
    regexOption.textContent = 'Regex Pattern';
    
    typeSelect.appendChild(keywordOption);
    typeSelect.appendChild(regexOption);
    typeSelect.value = type;
    
    // Update placeholder based on selected type
    typeSelect.addEventListener('change', function() {
        if (this.value === 'keyword') {
            patternInput.placeholder = 'Keyword (e.g., DOB)';
        } else {
            patternInput.placeholder = 'Regex pattern (e.g., \\d{4}\\s\\d{4}\\s\\d{4})';
        }
    });
    
    // Remove button
    const removeBtn = document.createElement('button');
    removeBtn.className = 'remove-field-btn';
    removeBtn.innerHTML = '&times;';
    removeBtn.addEventListener('click', function() {
        fieldsList.removeChild(fieldEntry);
    });
    
    // Add elements to field entry
    fieldEntry.appendChild(nameInput);
    fieldEntry.appendChild(patternInput);
    fieldEntry.appendChild(typeSelect);
    fieldEntry.appendChild(removeBtn);
    
    // Add field entry to the list
    fieldsList.appendChild(fieldEntry);
}

// Setup the extract text button
function setupExtractButton() {
    document.getElementById("uploadButton").addEventListener("click", async function() {
        const fileInput = document.getElementById("fileUpload");
        const outputText = document.getElementById("outputText");
        const uploadButton = document.getElementById("uploadButton");
        const downloadButton = document.getElementById("downloadButton");
        const downloadFieldsButton = document.getElementById("downloadFieldsButton");
        const languageSelect = document.getElementById("languageSelect");
        const processedImageContainer = document.getElementById("processedImageContainer");
        const processedImage = document.getElementById("processedImage");
        const extractedFieldsContainer = document.getElementById("extractedFieldsContainer");
        const extractedFieldsResults = document.getElementById("extractedFieldsResults");
        
        if (fileInput.files.length === 0) {
            alert("Please select a file first.");
            return;
        }
        
        // Prepare UI for processing
        outputText.value = "Processing...";
        uploadButton.disabled = true;
        downloadButton.style.display = "none";
        downloadFieldsButton.style.display = "none";
        processedImageContainer.style.display = "none";
        extractedFieldsContainer.style.display = "none";
        
        const formData = new FormData();
        formData.append("file", fileInput.files[0]);
        formData.append("language", languageSelect.value);
        
        // Add custom fields if enabled
        const enableCustomFields = document.getElementById('enableCustomFields').checked;
        console.log("Custom fields enabled:", enableCustomFields);
        
        if (enableCustomFields) {
            const customFields = getCustomFieldsData();
            console.log("Custom fields data:", customFields);
            
            if (Object.keys(customFields).length > 0) {
                // Convert to JSON string
                const customFieldsJson = JSON.stringify(customFields);
                console.log("Custom fields JSON:", customFieldsJson);
                
                // Add to form data
                formData.append("custom_fields", customFieldsJson);
                
                // Log all form data entries for debugging
                console.log("All form data entries:");
                for (let [key, value] of formData.entries()) {
                    console.log(`${key}: ${value}`);
                }
            }
        }
        
        try {
            console.log("Sending request to OCR endpoint...");
            const response = await fetch("http://127.0.0.1:8000/ocr", {
                method: "POST",
                body: formData,
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Server error: ${errorData.detail || response.statusText}`);
            }
            
            const result = await response.json();
            console.log("OCR result:", result);
            outputText.value = result.text || "No text found.";
            
            // Display processed image
            if (result.image) {
                processedImage.src = result.image;
                processedImageContainer.style.display = "block";
            }
            
            // Display extracted fields if any
            if (result.extracted_fields && Object.keys(result.extracted_fields).length > 0) {
                extractedFieldsResults.innerHTML = '';
                
                for (const [field, value] of Object.entries(result.extracted_fields)) {
                    const fieldElement = document.createElement('div');
                    fieldElement.className = 'field-result';
                    
                    const nameElement = document.createElement('div');
                    nameElement.className = 'field-name';
                    nameElement.textContent = field + ':';
                    
                    const valueElement = document.createElement('div');
                    valueElement.className = 'field-value';
                    valueElement.textContent = value;
                    
                    fieldElement.appendChild(nameElement);
                    fieldElement.appendChild(valueElement);
                    extractedFieldsResults.appendChild(fieldElement);
                }
                
                extractedFieldsContainer.style.display = 'block';
                downloadFieldsButton.style.display = 'inline-block';
            }
            
            // Reveal download button if text was successfully extracted
            if (result.text && result.text.trim().length > 0) {
                downloadButton.style.display = "inline-block";
            }
            
        } catch (error) {
            console.error("Error:", error);
            outputText.value = "Error extracting text. " + error.message;
        } finally {
            uploadButton.disabled = false;
        }
    });
}

// Get the custom fields data from the UI
function getCustomFieldsData() {
    const customFields = {};
    
    // Get all field entries
    const fieldEntries = document.querySelectorAll('.field-entry');
    fieldEntries.forEach(entry => {
        const nameInput = entry.querySelector('.field-name-input');
        const patternInput = entry.querySelector('.field-pattern-input');
        const typeSelect = entry.querySelector('.field-type-select');
        
        const name = nameInput.value.trim();
        const pattern = patternInput.value.trim();
        const type = typeSelect.value;
        
        if (name && pattern) {
            if (type === 'regex') {
                customFields[name] = `regex:${pattern}`;
            } else {
                customFields[name] = pattern;
            }
        }
    });
    
    return customFields;
}

// Set up download buttons
function setupDownloadButtons() {
    // Download full text
    document.getElementById("downloadButton").addEventListener("click", function() {
        const text = document.getElementById("outputText").value;
        downloadTextFile(text, 'extracted_text.txt');
    });
    
    // Download extracted fields as JSON
    document.getElementById("downloadFieldsButton").addEventListener("click", function() {
        const fieldsContainer = document.getElementById("extractedFieldsResults");
        const fieldResults = fieldsContainer.querySelectorAll('.field-result');
        
        const extractedData = {};
        fieldResults.forEach(field => {
            const nameElem = field.querySelector('.field-name');
            const valueElem = field.querySelector('.field-value');
            
            if (nameElem && valueElem) {
                const name = nameElem.textContent.replace(':', '').trim();
                const value = valueElem.textContent.trim();
                extractedData[name] = value;
            }
        });
        
        const jsonStr = JSON.stringify(extractedData, null, 2);
        downloadTextFile(jsonStr, 'extracted_fields.json', 'application/json');
    });
}

// Helper function to download text as a file
function downloadTextFile(text, filename, mimeType = 'text/plain') {
    if (text.trim().length > 0) {
        const blob = new Blob([text], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}