// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
		interface Locals {
			user: {
				id: number;
				username: string;
				email: string;
				role: string;
			} | null;
		}

		interface Session {
			user: {
				id: number;
				username: string;
				email: string;
				role: string;
			} | null;
		}
	}
}


export {};
