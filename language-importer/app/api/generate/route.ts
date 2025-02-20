import { openai } from "@ai-sdk/openai"
import { generateText } from "ai"

export async function POST(req: Request) {
  if (!process.env.OPENAI_API_KEY) {
    return Response.json({ error: "OpenAI API key is not configured" }, { status: 500 })
  }

  try {
    const { categories } = await req.json()

    if (!categories || categories.length === 0) {
      return Response.json({ error: "At least one category is required" }, { status: 400 })
    }

    const prompt = `Generate a comprehensive list of Spanish vocabulary words related to the following themes: ${categories.join(", ")}. 
    The output should be a JSON object where each key is a category and its value is an array of vocabulary items.
    Each vocabulary item in the array should be an object containing:
    - spanish: the Spanish word
    - english: the English translation
    - parts: an object containing:
      - category: the part of speech (noun, verb, adjective, etc.)
      - type: subcategory or specific usage
      - formality: formal, informal, or neutral
    
    Generate at least 5 relevant words for each category. Ensure the output is valid JSON without any markdown formatting.`

    const { text } = await generateText({
      model: openai("gpt-4o"),
      prompt,
      system:
        "You are a helpful language learning assistant that generates vocabulary lists in JSON format. Always ensure the output is valid JSON.",
    })

    try {
      // Parse the response to ensure it's valid JSON
      const jsonResponse = JSON.parse(text)

      // Validate that each category has at least 5 words
      for (const category in jsonResponse) {
        if (jsonResponse[category].length < 5) {
          throw new Error(`Category '${category}' has fewer than 5 words`)
        }
      }

      return Response.json(jsonResponse)
    } catch (parseError) {
      console.error("Failed to parse or validate JSON response:", text)
      return Response.json({ error: "Failed to generate valid vocabulary response" }, { status: 500 })
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : "An unknown error occurred"
    console.error("API Error:", errorMessage)
    return Response.json({ error: "Failed to generate vocabulary: " + errorMessage }, { status: 500 })
  }
}

