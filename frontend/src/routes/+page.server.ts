// frontend/src/routes/+page.server.ts
import type { Actions, PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ locals }) => {
	if (locals.user) {
		throw redirect(302, '/dashboard');
	} else {
		throw redirect(302, '/login');
	}
};
