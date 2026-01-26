import { Router } from "express";
import {
  signup,
  signin,
  getCurrentUser,
} from "../controllers/auth.controllers.js";
import {
  startOAuth,
  handleOAuthCallback,
  oauthStatus,
} from "../controllers/oauth.controllers.js";
import { verifyJWT } from "../middleware/auth.middleware.js";

const router = Router();

router.post("/signup", signup);

router.post("/signin", signin);
router.get("/me", verifyJWT, getCurrentUser);
router.get("/oauth/status", oauthStatus);
router.get("/oauth/:provider", startOAuth);
router.get("/oauth/:provider/callback", handleOAuthCallback);

export default router;
