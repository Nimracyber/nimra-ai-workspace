import { NextResponse } from 'next/server';
import ollama from 'ollama';

export async function POST(request) {
  try {
    const { prompt } = await request.json();

    if (!prompt) {
      return NextResponse.json({ error: 'Prompt is missing.' }, { status: 400 });
    }

    const response = await ollama.generate({
      model: 'nimra-ai',
      prompt: prompt,
      stream: false, 
    });

    return NextResponse.json({ response: response.response }, { status: 200 });

  } catch (error) {
    return NextResponse.json(
      { detail: 'Make sure your background terminal is running "ollama run nimra-ai".' },
      { status: 500 }
    );
  }
}