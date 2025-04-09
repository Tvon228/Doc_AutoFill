import { Component, Show } from "solid-js"
import { Router, Route, Navigate } from "@solidjs/router"
import classes from "./App.module.sass"
import DocView from "./components/DocView"
import MyDocs from "./components/MyDocuments"
import WorkArea from "./components/WorkArea"
import Header from "./components/layout/header"
import { auth } from "./stores/auth.store"
import AuthPage from "./components/Auth/page"

const App: Component = () => {
	return (
		<Router>
			<Route
				path="/"
				component={() => (
					<Show when={auth.isAuthenticated} fallback={<AuthPage />}>
						<Navigate href="/app" />
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
					</Show>
				)}
			/>
		</Router>
	)
}

export default App
