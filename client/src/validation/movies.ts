import z from 'zod';

export const createRatingSchema = z.object({
  rating: z.number({ message: 'Rating is required' }).min(1).max(10),
});

export type ICreateRating = z.infer<typeof createRatingSchema>;
