export const fetcher = async (url: string, token: string) => {
    const res = await fetch(url, {
        headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
        },
    });

    if (!res.ok) {
        throw new Error("An error occurred while fetching the data.");
    }

    return res.json();
};
