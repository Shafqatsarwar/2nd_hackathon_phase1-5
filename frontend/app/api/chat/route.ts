import { NextRequest } from "next/server";
import { StreamingTextResponse } from "ai";

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
    try {
        const { messages, userId, token } = await req.json();

        if (!messages || messages.length === 0) {
            return new Response("No messages provided", { status: 400 });
        }

        const lastMessage = messages[messages.length - 1];
        // Use INTERNAL_BACKEND_URL for container-to-container, fallback to Public/Localhost
        const backendUrl = process.env.INTERNAL_BACKEND_URL || process.env.NEXT_PUBLIC_BACKEND_URL || "http://todo-app-backend-service:8000";

        // Call backend chat endpoint
        const response = await fetch(`${backendUrl}/api/${userId}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token || "admin_token"}`
            },
            body: JSON.stringify({
                message: lastMessage.content,
                conversation_id: null
            })
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Backend chat error:", errorText);

            // Return a user-friendly error message
            const errorMessage = response.status === 500
                ? "I'm having trouble connecting to the AI service. Please make sure the backend is running and OPENAI_API_KEY is configured."
                : `Backend error: ${errorText}`;

            // Return as AI SDK compatible stream
            const encoder = new TextEncoder();
            const stream = new ReadableStream({
                start(controller) {
                    const formattedError = `0:"${errorMessage.replace(/"/g, '\\"').replace(/\n/g, '\\n')}"\n`;
                    controller.enqueue(encoder.encode(formattedError));
                    controller.close();
                }
            });

            return new StreamingTextResponse(stream);
        }

        // Backend returns plain text stream, we need to convert it properly
        if (!response.body) {
            throw new Error("No response body from backend");
        }

        // Create a readable stream that properly formats the backend response
        // The AI SDK expects data in the format: "0:\"text\"\n"
        const encoder = new TextEncoder();
        const decoder = new TextDecoder();

        const transformedStream = new ReadableStream({
            async start(controller) {
                const reader = response.body!.getReader();

                try {
                    while (true) {
                        const { done, value } = await reader.read();

                        if (done) {
                            controller.close();
                            break;
                        }

                        // Decode the chunk
                        const text = decoder.decode(value, { stream: true });
                        if (text) {
                            // Format each chunk according to AI SDK data stream protocol
                            // Format: "0:\"text content\"\n"
                            const formattedChunk = `0:"${text.replace(/"/g, '\\"').replace(/\n/g, '\\n')}"\n`;
                            controller.enqueue(encoder.encode(formattedChunk));
                        }
                    }
                } catch (error) {
                    console.error("Stream processing error:", error);
                    controller.error(error);
                }
            }
        });

        return new StreamingTextResponse(transformedStream);

    } catch (error: any) {
        console.error("Chat API Error:", error);

        // Return error as AI SDK compatible stream
        const encoder = new TextEncoder();
        const stream = new ReadableStream({
            start(controller) {
                const errorMsg = "I'm having trouble processing your request. Please ensure the backend server is running at " +
                    (process.env.NEXT_PUBLIC_BACKEND_URL || "http://todo-app-backend-service:8000");
                const formattedError = `0:"${errorMsg.replace(/"/g, '\\"').replace(/\n/g, '\\n')}"\n`;
                controller.enqueue(encoder.encode(formattedError));
                controller.close();
            }
        });

        return new StreamingTextResponse(stream);
    }
}
