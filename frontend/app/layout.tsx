import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: "The Evolution of Todo",
    description: "AI-powered todo application with voice support and Kubernetes deployment",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    );
}
