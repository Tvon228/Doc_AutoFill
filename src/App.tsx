import { Component, Show } from "solid-js"
import { Router, Route, Navigate } from "@solidjs/router"

import classes from "./App.module.sass"

import Header from "./components/layout/header"
import DocView from "./components/DocView"
import MyDocs from "./components/MyDocuments"
import WorkArea from "./components/WorkArea"

import AuthPage from "./components/Auth/page"
import ProfilePage from "./components/Profile"
import TempAdminPage from "./components/Admin/TempAdminPage"

import { auth } from "./stores/authStore"

const App: Component = () => {
	return (
		<Router>
			{/* Главный маршрут */}
			<Route
				path="/"
				component={() => (
					<Show
						when={!auth.isAuthenticated}
						fallback={
							<Navigate
								href={
									auth.user?.role === "admin"
										? "/admin"
										: "/app"
								}
							/>
						}
					>
						<AuthPage />
					</Show>
				)}
			/>

			{/* Панель администратора */}
			<Route
				path="/admin"
				component={() => (
					<Show
						when={
							auth.isAuthenticated && auth.user?.role === "admin"
						}
						fallback={<Navigate href="/" />}
					>
						<TempAdminPage />
					</Show>
				)}
			/>

			{/* Панель пользователя */}
			<Route
				path="/app"
				component={() => (
					<Show
						when={
							auth.isAuthenticated && auth.user?.role === "user"
						}
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

			<Route
				path="/profile"
				component={() => (
					<Show
						when={auth.isAuthenticated}
						fallback={<Navigate href="/" />}
					>
						<div class={classes.header}>
							<Header />
						</div>
						<div class={classes.content}>
							<div class={classes.profilePage}>
								<MyDocs />
								<ProfilePage />
								<div class={classes.place}/>
							</div>
						</div>
					</Show>
				)}
			/>
		</Router>
	)
}

export default App
