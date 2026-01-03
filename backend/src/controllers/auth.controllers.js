import asyncHandler from "../utils/asyncHandler.js";
import ApiError from "../utils/ApiError.js";
import ApiResponse from "../utils/ApiResponse.js";
import User from "../models/user.model.js";
import generateToken from "../utils/jwt.js";

const signup = asyncHandler(async (req, res) => {
  console.log('🚀 SIGNUP CONTROLLER HIT');
  console.log('📝 Request body:', req.body);
  
  try {
    const { username, email, password } = req.body;
    console.log('📋 Extracted fields:', { username, email, password: password ? '***' : 'undefined' });

    if ([username, email, password].some((field) => field?.trim() === "")) {
      console.log('❌ Validation failed: Empty fields');
      throw new ApiError(400, "All fields are required");
    }

    console.log('🔍 Checking for existing user...');
    const existedUser = await User.findOne({
      $or: [{ email }],
    });
    console.log('👤 Existing user result:', existedUser);
    
    if (existedUser) {
      console.log('❌ User already exists');
      throw new ApiError(409, "User with email or username already exists");
    }

    console.log('👤 Creating new user...');
    const newUser = await User.create({
      username,
      email,
      password,
    });
    console.log('✅ New user created:', newUser);

    const createdUser = await User.findById(newUser._id).select("-password");
    console.log('👤 User fetched without password:', createdUser);

    if (!createdUser) {
      console.log('❌ Failed to fetch created user');
      throw new ApiError(500, "Something went wrong while registering the user");
    }
    
    console.log('🔑 Generating JWT token...');
    const jwtToken = generateToken(createdUser);
    console.log('✅ JWT token generated');
    
    console.log('📤 Sending success response...');
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
    console.error('❌ SIGNUP ERROR:', error);
    console.error('❌ Error stack:', error.stack);
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
