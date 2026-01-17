import { getToken } from "./auth";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api";

export interface SavedCoverLetter {
    _id: string;
    userId: string;
    companyName: string;
    jobTitle: string;
    jobDescription?: string;
    tone: "formal" | "confident" | "friendly";
    coverLetter: {
        greeting: string;
        body: string[];
        closing: string;
        signOff: string;
        candidateName?: string;
    };
    createdAt: string;
    updatedAt: string;
}

export interface SaveCoverLetterRequest {
    companyName: string;
    jobTitle: string;
    jobDescription?: string;
    tone: "formal" | "confident" | "friendly";
    coverLetter: {
        greeting: string;
        body: string[];
        closing: string;
        signOff: string;
        candidateName?: string;
    };
}

/**
 * Save a generated cover letter to the database
 */
export async function saveCoverLetter(
    data: SaveCoverLetterRequest
): Promise<SavedCoverLetter> {
    const token = getToken();

    if (!token) {
        throw new Error("You must be logged in to save cover letters");
    }

    const response = await fetch(`${API_BASE_URL}/cover-letters`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(data),
    });

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.message || "Failed to save cover letter");
    }

    return result.data.coverLetter;
}

/**
 * Get all saved cover letters for the current user
 */
export async function getMyCoverLetters(): Promise<SavedCoverLetter[]> {
    const token = getToken();

    if (!token) {
        throw new Error("You must be logged in to view your cover letters");
    }

    const response = await fetch(`${API_BASE_URL}/cover-letters`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
    });

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.message || "Failed to fetch cover letters");
    }

    return result.data.coverLetters;
}

/**
 * Get a single cover letter by ID
 */
export async function getCoverLetterById(id: string): Promise<SavedCoverLetter> {
    const token = getToken();

    if (!token) {
        throw new Error("You must be logged in to view this cover letter");
    }

    const response = await fetch(`${API_BASE_URL}/cover-letters/${id}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
    });

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.message || "Failed to fetch cover letter");
    }

    return result.data.coverLetter;
}

/**
 * Delete a cover letter by ID
 */
export async function deleteCoverLetter(id: string): Promise<void> {
    const token = getToken();

    if (!token) {
        throw new Error("You must be logged in to delete cover letters");
    }

    const response = await fetch(`${API_BASE_URL}/cover-letters/${id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
    });

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.message || "Failed to delete cover letter");
    }
}
