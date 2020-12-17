# Coffee Shop Frontend

## Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). It is recommended you stand up the backend first, test using Postman, and then the frontend should integrate smoothly.

### Installing Dependencies

#### Installing Node and NPM

This project depends on the **Node.js** and **Node Package Manager** (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing Ionic CLI

The **Ionic Command Line Interface** is required to serve and build the frontend. Instructions for installing the CLI are in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).

#### Installing project dependencies

This project uses the **NPM** to manage software dependencies. The NPM relies on the **package.json** file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

## Tasks performed

### Configure Environment Variables

**Ionic** uses a configuration file to manage the environment variables. These variables ship with the transpiled software and should not include secrets.

- Ensured that each variable in `./src/environments/environments.ts` reflects the system stood up for the backend.

## Running the Frontend in Dev Mode

**Ionic** ships with a useful development server which detects changes and transpiles the work. The application is then accessible through the browser on a localhost port. To run the development server, `cd` into the `frontend` directory and run:

```bash
ionic serve
```

>_tip_: Do not use **ionic serve**  in production. Instead, build Ionic into a build artifact for your desired platforms.
[Checkout the Ionic docs to learn more](https://ionicframework.com/docs/cli/commands/build)

## Key Aspects of the Software Design

The two key areas of the frontend framework relevant here are:

### Authentication

The authentication system used for this project is **Auth0**. `./src/services/auth.service.ts` contains the logic to direct a user to the Auth0 login page, manage the JSON Web Token (JWT) upon successful callback, and handle setting and retrieving the token from the local store. This token is then consumed by the DrinkService (`./src/services/auth.service.ts`) and passed as an Authorization header when making the requests to the backend.

### Authorization

The **Auth0 JSON Web Token** (JWT) includes claims for permissions based on the user's role within the Auth0 system. This project makes use of these claims using the `auth.can(permission)` method which checks if particular permissions exist within the JWT permissions claim of the currently logged in user. This method is defined in `./src/services/auth.service.ts` and is then used to enable and disable buttons in `./src/pages/drink-menu/drink-form/drink-form.html`.
