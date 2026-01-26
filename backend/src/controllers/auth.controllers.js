import asyncHandler from "../utils/asyncHandler.js";
import ApiError from "../utils/ApiError.js";
import ApiResponse from "../utils/ApiResponse.js";
import User from "../models/user.model.js";
import generateToken from "../utils/jwt.js";

const signup = asyncHandler(async (req, res) => {
  try {
    const { username, email, password } = req.body;

    if ([username, email, password].some((field) => field?.trim() === "")) {
      throw new ApiError(400, "All fields are required");
    }

    const existedUser = await User.findOne({
      $or: [{ email }],
    });
    
    if (existedUser) {
      throw new ApiError(409, "User with email or username already exists");
    }

    const newUser = await User.create({
      username,
      email,
      password,
    });

    const createdUser = await User.findById(newUser._id).select("-password");

    if (!createdUser) {
      throw new ApiError(500, "Something went wrong while registering the user");
    }
    
    const jwtToken = generateToken(createdUser);
    
    return res
      .status(201)
      .json(
        new ApiResponse(
          201,
          { user: createdUser, jwtToken },
          "User registered Successfully",
        ),
      );
  } catch (error) {
    return res.status(500).json({
      success: false,
      message: error.message || "Server error"
    });
  }
});

const signin = asyncHandler(async (req, res) => {
  const { email, password } = req.body;

  if (!email) {
    throw new ApiError(400, "email is required");
  }

  const user = await User.findOne({
    email,
  });

  if (!user) {
    throw new ApiError(404, "User does not exist");
  }

  const isPasswordValid = await user.isPasswordCorrect(password);

  if (!isPasswordValid) {
    throw new ApiError(401, "Invalid user credentials");
  }
  const jwtToken = generateToken(user);

  const loggedInUser = await User.findById(user._id).select("-password");

  const options = {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
  };

  return res
    .status(200)
    .cookie("jwtToken", jwtToken, options)
    .json(
      new ApiResponse(
        200,
        {
          user: loggedInUser,
          jwtToken,
        },
        "User logged In Successfully",
      ),
    );
});

const getCurrentUser = asyncHandler(async (req, res) => {
  return res
    .status(200)
    .json(
      new ApiResponse(200, { user: req.user }, "User fetched successfully"),
    );
});

export { signup, signin, getCurrentUser };
