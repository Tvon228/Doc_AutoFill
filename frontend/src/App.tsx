import { Component, Show } from "solid-js";
import classes from "./App.module.sass";

import Header from "./components/layout/header";
import MyDocs from "./components/MyDocuments";
import WorkArea from "./components/WorkArea";
import DocView from "./components/DocView";

import { auth } from "./stores/authStore";

import AuthPage from "./components/Auth/page";
import { Navigate, Route, Router } from "@solidjs/router";

const AppInterface = () => {
  return (
    <>
      <div class={classes.header}>
        <Header />
      </div>
      <div class={classes.content}>
        <div class={classes.main}>
          <MyDocs />
          <WorkArea />
          <DocView />
        </div>
      </div>
    </>
  );
};

const App: Component = () => {
	return (
		<Router>
			<Route
				path="/"
				component={() => (
					<Show
						when={!auth.isAuthenticated}
						fallback={<Navigate href="/app" />}
					>
						<AuthPage />
					</Show>
				)}
			/>

			<Route
				path="/app"
				component={() => (
					<Show
						when={auth.isAuthenticated}
						fallback={<Navigate href="/" />}
					>
						<AppInterface />
					</Show>
				)}
			/>

			{/* Обработка неизвестных путей */}
			<Route path="*" component={() => <Navigate href="/" />} />
		</Router>
	);
};

export default App;