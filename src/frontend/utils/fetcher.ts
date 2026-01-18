export const fetcher = async (url: string, token: string) => {
    const res = await fetch(url, {
        headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
        },
    });

    if (!res.ok) {
        const errorText = await res.text().catch(() => "No error body");
        throw new Error(`Error ${res.status} fetching ${url}: ${errorText}`);
    }

    return res.json();
};
