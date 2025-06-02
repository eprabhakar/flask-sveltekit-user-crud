// src/routes/+layout.server.ts
import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: LayoutServerLoad = async ({ locals }) => {
	if (locals.user) {
		return {
			user: locals.user
		};
	}

	// No need to redirect here, just return null user
	return {
		user: null
	};
};
