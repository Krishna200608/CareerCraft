import { Router } from "express";
import {
    saveCoverLetter,
    getMyCoverLetters,
    getCoverLetterById,
    deleteCoverLetter,
} from "../controllers/coverLetter.controller.js";
import { verifyJWT } from "../middleware/auth.middleware.js";

const router = Router();

// All routes require authentication
router.use(verifyJWT);

// POST /api/cover-letters - Save a new cover letter
router.post("/", saveCoverLetter);

// GET /api/cover-letters - Get all cover letters for the user
router.get("/", getMyCoverLetters);

// GET /api/cover-letters/:id - Get a specific cover letter
router.get("/:id", getCoverLetterById);

// DELETE /api/cover-letters/:id - Delete a cover letter
router.delete("/:id", deleteCoverLetter);

export default router;
