import z from 'zod';

export const updateSchema = z.object({
  email: z.email(),
});

export type IUpdate = z.infer<typeof updateSchema>;
