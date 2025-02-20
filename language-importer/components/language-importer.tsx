"use client"

import type React from "react"
import { useState } from "react"
import { Loader2, Book, Copy, CheckCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { toast } from "@/components/ui/use-toast"
import { Toaster } from "@/components/ui/toaster"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export function LanguageImporter() {
  const [categories, setCategories] = useState("")
  const [result, setResult] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isCopied, setIsCopied] = useState(false)

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setIsLoading(true)
    setResult("")
    setIsCopied(false)

    try {
      const categoryList = categories
        .split(",")
        .map((cat) => cat.trim())
        .filter(Boolean)

      if (categoryList.length === 0) {
        throw new Error("Please enter at least one category")
      }

      const response = await fetch("/api/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ categories: categoryList }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || "Failed to generate vocabulary")
      }

      setResult(JSON.stringify(data, null, 2))
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "An unknown error occurred"
      console.error("Error:", errorMessage)
      toast({
        title: "Error",
        description: errorMessage,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const copyToClipboard = () => {
    navigator.clipboard.writeText(result)
    setIsCopied(true)
    toast({
      title: "Copied!",
      description: "The vocabulary list has been copied to your clipboard.",
    })
    setTimeout(() => setIsCopied(false), 2000)
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Book className="w-6 h-6 text-blue-600" />
          Generate Vocabulary
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-8">
        <form onSubmit={onSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="categories">Thematic Categories</Label>
            <Input
              id="categories"
              placeholder="Enter categories separated by commas (e.g., 'food, colors, greetings')"
              value={categories}
              onChange={(e) => setCategories(e.target.value)}
              required
              className="w-full"
            />
          </div>
          <Button type="submit" disabled={isLoading} className="w-full">
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating...
              </>
            ) : (
              "Generate Vocabulary"
            )}
          </Button>
        </form>

        {result && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <Label>Generated Vocabulary</Label>
              <Button variant="outline" onClick={copyToClipboard} disabled={isCopied}>
                {isCopied ? (
                  <>
                    <CheckCircle className="mr-2 h-4 w-4 text-green-500" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="mr-2 h-4 w-4" />
                    Copy to Clipboard
                  </>
                )}
              </Button>
            </div>
            <Textarea value={result} readOnly className="min-h-[400px] font-mono text-sm" />
          </div>
        )}
      </CardContent>
      <Toaster />
    </Card>
  )
}

