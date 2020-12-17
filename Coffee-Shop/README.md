## Coffee Shop

The Coffee Shop application allows for:

1) Displaying the graphics representing the ratios of ingredients in each drink.
2) Public users can view the names of the drinks and the graphics.
3) The shop baristas can see the recipe information.
4) The shop managers can create new drinks and edit the existing drinks.

### Backend

The `./backend` directory contains a **Flask** server with a **SQLAlchemy** module to simplify the data needs. The application uses **Auth0** for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete **Ionic** frontend to consume the data from the **Flask** server. The environment variables found within (./frontend/src/environment/environment.ts) reflect the **Auth0** configuration details set up for the backend app. 

[View the README.md within ./frontend for more details.](./frontend/README.md)
