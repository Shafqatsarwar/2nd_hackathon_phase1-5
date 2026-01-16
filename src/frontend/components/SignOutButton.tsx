"use client";

import { createAuthClient } from "better-auth/react";
import { useRouter } from "next/navigation";

const authClient = createAuthClient();

export default function SignOutButton() {
    const router = useRouter();

    const handleSignOut = async () => {
        await authClient.signOut();
        router.push("/");
    };

    return (
        <button
            onClick={handleSignOut}
            className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
        >
            Sign Out
        </button>
    );
}
