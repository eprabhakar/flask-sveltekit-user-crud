// src/routes/+layout.server.ts
import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';
 

export const load: LayoutServerLoad = async ({ locals }) => {
	if (!locals.user) {
		throw redirect(302, '/login');
	} else{
		return {
			user: locals.user ?? { username: 'Guest', avatar: null }
		};
	}

	// No need to redirect here, just return null user
	return {
		user: null
	};
};
