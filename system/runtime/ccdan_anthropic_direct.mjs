#!/usr/bin/env node
import fs from "node:fs/promises";

const [requestPath, sourcePath, model = "claude-opus-4-6"] = process.argv.slice(2);
const apiKey = process.env.CCDAN_API_KEY;
if (!requestPath || !sourcePath || !apiKey) process.exit(2);

const [request, source] = await Promise.all([fs.readFile(requestPath, "utf8"), fs.readFile(sourcePath, "utf8")]);
const abort = new AbortController();
const timer = setTimeout(() => abort.abort(), 15 * 60 * 1000);
try {
  const response = await fetch("https://ai.ccdan.live/v1/messages", {
    method: "POST",
    signal: abort.signal,
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "Content-Type": "application/json",
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model,
      max_tokens: 12000,
      system: "Read the complete source text in the user message. Return exactly one contract JSON object, without Markdown, explanation, or tool narration.",
      messages: [{ role: "user", content: `${request}\n\nCOMPLETE NORMALIZED SOURCE TEXT:\n${source}` }],
    }),
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(JSON.stringify(payload));
  const output = (payload.content ?? []).filter((item) => item.type === "text").map((item) => item.text).join("\n").trim();
  if (!output) throw new Error("empty CCDAN Anthropic response");
  process.stdout.write(`${output}\n`);
} finally {
  clearTimeout(timer);
}
