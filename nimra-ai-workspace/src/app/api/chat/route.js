import { NextResponse } from 'next/server';
import Groq from 'groq-sdk';

export async function POST(req) {
  try {
    const groq = new Groq({
      apiKey: process.env.GROQ_API_KEY,
    });

    const { messages } = await req.json();

    const systemPrompt = {
      role: 'system',
      content: `You are a highly personalized, brilliant, and supportive AI companion tailored specifically for your user. You must always maintain this context and never break character.
      
      Here is the essential information about your user that you must remember perfectly:
      - Name: Nimra Farooqi
      - Age: 25 years old (born July 1, 2000)
      - Education: Master of Science (M.Sc.) in Mathematics from the University of Gujrat, Bachelor of Science in Double Mathematics and Physics, and F.Sc. in Pre-Engineering.
      - Hometown: Chakwal, Pakistan (frequently commutes to Islamabad/Rawalpindi for professional training and exams).
      - Professional Background: Experienced in data analytics, machine learning, and quantitative programming (Python, SQL, Pandas, Scikit-learn, Power BI, FastAPI, Next.js, and computer vision tools like OpenCV and YOLO). Also studied ICAP PRC modules and competitive civil service exam syllabi (CSS/PMS).`
    };

    const completion = await groq.chat.completions.create({
      model: 'llama-3.3-70b-versatile',
      messages: [systemPrompt, ...messages],
      temperature: 0.7,
    });

    const reply = completion.choices[0]?.message?.content || "I couldn't generate a response.";

    return NextResponse.json({ reply });
  } catch (error) {
    console.error('Groq API Error:', error);
    return NextResponse.json({ error: 'Failed to fetch response from AI' }, { status: 500 });
  }
}