# Module 12 Reflection: User and Calculation Routes + Integration Testing

For Module 12, I continued working on my FastAPI calculator from Module 11. This time I learned how to add routes so users can register, log in, and work with calculations. I also learned how to use the calculation endpoints to add, view, edit, and delete information saved in PostgreSQL. At first, I was confused about how the routes, models, and database all connected, but testing each part helped me understand it better.

One challenge I had was getting Docker Desktop to start. I had to fix that problem before I could run my application. After Docker was working, I opened FastAPI Swagger in my browser and successfully tested user registration and login. I also ran the automated tests, and all 26 tests passed locally.

Another problem happened when I uploaded the project to GitHub. My GitHub Actions workflow failed because the Docker Hub username and token were not set up correctly. I added the correct GitHub settings and reran the workflow. This time it finished successfully with a green check mark.

Overall, this module showed me why testing is important and how GitHub Actions can automatically test and build an application. I still had to go back and fix errors, but I feel more comfortable using FastAPI, PostgreSQL, Docker, and GitHub Actions than I did at the beginning of the course.
