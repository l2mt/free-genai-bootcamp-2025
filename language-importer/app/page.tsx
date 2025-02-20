import { LanguageImporter } from "@/components/language-importer"

export default function Home() {
  return (
    <main className="min-h-screen p-8 bg-gradient-to-b from-blue-100 to-white">
      <div className="max-w-3xl mx-auto space-y-8">
        <h1 className="text-4xl font-bold text-center text-blue-800">English-Spanish Vocabulary Generator</h1>
        <p className="text-center text-gray-600">Generate comprehensive vocabulary lists for multiple categories</p>
        <LanguageImporter />
      </div>
    </main>
  )
}

