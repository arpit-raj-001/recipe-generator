# recipe-generator
a website to generate recipes on the go with ai-powered generation tools , that gives ingredients and instructions in a json format which afterwords can be copied directly to the clipboard

acess the website from the following link given below , loading the website might take 1 to 2 minutes on your browser

https://recipe-generator-bdqi.onrender.com


✨ **Features**

- **Multi-Model Support:** Seamlessly switch between the Hugging Face `SmolLM3-3B` model and a powerful Groq-hosted model (`openai/gpt-oss-20b`).  
- **Structured Output:** Prompts are engineered to force the LLM to return a clean JSON object with predefined fields (`name`, `ingredients`, `instructions`, `prep_time`, etc.).  
- **Performance Benchmarking:** Automatically tracks and displays the generation time for each model, allowing for direct performance comparison.  
- **Robust Error Handling:** Includes custom backend logic to extract and parse JSON even if the LLM includes surrounding text or errors.  
- **User Interface:** A single-page, responsive HTML/CSS/JavaScript front-end to interact with the API.  

 **Technology Stack**

| Component       | Technology / Tool                      | Role                                                                 |
|-----------------|---------------------------------------|----------------------------------------------------------------------|
| **Backend**     | Python, Flask                          | REST API framework and serves the front-end                          |
| **LLM Integration** | LangChain (ChatHuggingFace), Groq SDK | Handles model connections, prompting, and response invocation       |
| **LLMs Used**   | Hugging Face: `HuggingFaceTB/SmolLM3-3B` | Open-source, self-hosted option (via API)                            |
|                 | Groq: `openai/gpt-oss-20b`            | High-speed, commercial LLM inference                                  |
| **Frontend**    | HTML, CSS, Vanilla JavaScript          | User input, model selection, and formatted display of JSON results  |



# Project Discussion

## What I Learned
This project provided crucial hands-on experience in building a reliable, LLM-powered application:

### Structured Output Engineering
The core challenge was forcing the LLMs to return a clean, predictable JSON object. I learned that highly descriptive and restrictive instructions in the prompt (e.g., "Return only valid JSON with fields...") are non-negotiable for reliable API integration.

### Robust Error Handling in Production (continued)
To extract the JSON object from the raw model response, I implemented post-processing logic. This addresses a common real-world issue where LLMs might add conversational text or tags (like `<thought>` or `\n```json`) around the JSON, which would otherwise cause the standard `json.loads()` to fail.

### Model Interoperability
I gained practical experience connecting to different providers—LangChain for Hugging Face and the native SDK for Groq—highlighting the convenience of LangChain's standardized interface versus the direct access and control offered by a native SDK.

---

## Which Model Performed Better and Why
The Groq-hosted model (`openai/gpt-oss-20b`) performed significantly better than the Hugging Face model (`SmolLM3-3B`).

### Performance Comparison

| Metric                 | Hugging Face (SmolLM3-3B)        | Groq (gpt-oss-20b)               |
|------------------------|---------------------------------|---------------------------------|
| Inference Speed        | Slower (Often 10+ seconds)      | Ultra-Fast (Typically 1-3 seconds) |
| JSON Consistency       | Moderate (Frequently required manual extraction) | High (Consistently returned cleaner JSON) |
| Recipe Detail          | Good                             | Excellent                        |

### Reason for Superior Performance
- **Speed:** Groq's specialized LPU (Language Processing Unit) architecture is designed for low-latency inference, delivering results much faster than traditional GPUs used by the Hugging Face endpoint. This speed is critical for a good web application user experience.  Each LPU is functionally sliced, meaning it’s broken into units that can process instructions simultaneously and parallely



---





## Sample response (grok openai/gpt-oss-20b)

# 📝 Kurukure Momos

A crispy, deep-fried take on the classic momo dumpling. These momos are filled with a savory meat and vegetable mixture, sealed with a dough wrapper, and coated in a light flour-cornstarch batter before being fried to a golden-brown crisp.

---

## ⏱️ Prep Time
30 minutes

## 🔥 Cook Time
15 minutes

## 🍽️ Servings
4-6

## 📊 Difficulty
Medium

---

## 🥘 Ingredients

### Dough
- 1 cup all-purpose flour, plus extra for dusting  
- 1/4 teaspoon salt  
- 1/2 cup warm water  
- 1 tablespoon vegetable oil  

### Filling
- 1 pound ground pork (or ground chicken)  
- 1 cup finely chopped cabbage  
- 1/2 cup finely chopped carrots  
- 1/4 cup chopped green onions  
- 2 cloves garlic, minced  
- 1 teaspoon ginger, grated  
- 1 tablespoon soy sauce  
- 1 tablespoon oyster sauce  
- 1 teaspoon sesame oil  
- 1/2 teaspoon ground black pepper  

### Coating
- 2 tablespoons cornstarch  
- 1 tablespoon all-purpose flour  
- 1/2 teaspoon baking powder  
- 1/4 teaspoon salt  
- 1/4 teaspoon ground white pepper  

### Batter
- 1 cup water  
- 1 tablespoon all-purpose flour  
- 1/2 teaspoon baking soda  

### For Frying
- Oil for deep frying

---

## 👨‍🍳 Instructions

1. **Prepare the dough:** In a large bowl, combine 1 cup flour, 1/4 teaspoon salt, warm water, and 1 tablespoon oil. Knead until smooth and elastic. Cover and let rest for 20 minutes.

2. **Make the filling:** In a separate bowl, mix ground pork, cabbage, carrots, green onions, garlic, ginger, soy sauce, oyster sauce, sesame oil, and black pepper until well combined.

3. **Shape the momos:** Divide the rested dough into golf-ball sized portions. Roll each into a 3-inch circle. Place a tablespoon of filling in the center, fold over, pinch edges tightly, and form a half-moon shape.

4. **Prepare the coating:** Heat oil in a deep pan to 350°F (175°C). In a shallow bowl, combine 2 tablespoons cornstarch, 1 tablespoon flour, 1/2 teaspoon baking powder, 1/4 teaspoon salt, and 1/4 teaspoon white pepper.

5. **Coat the momos:** Lightly press each momo into the coating mixture until evenly coated on all sides.

6. **Prepare the batter:** Mix water, 1 tablespoon flour, and 1/2 teaspoon baking soda. Dip each coated momo into the batter and shake off excess.

7. **Fry the momos:** Carefully slide the batter-coated momos into hot oil. Fry in batches, turning occasionally, until golden brown and crispy (about 2–3 minutes per batch).

8. **Drain and serve:** Remove with a slotted spoon and drain on paper towels.

9. **Serve hot:** Pair with a dipping sauce made of soy sauce, chili oil, and a splash of rice vinegar.

---



## sample response (hugging face/smollm-3) 

i ran out of free api key acess for this month , ill update the document with a sample response of this model next month , note that the model was working before the limit reached and i have properly noted and documented my analysis




## Conclusion
For production use where speed and reliability are paramount, the Groq integration was the clear winner, demonstrating the value of high-performance LLM infrastructure.
