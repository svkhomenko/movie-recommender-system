import z from 'zod';
import { PASSWORD_LENGTH } from '~/consts/validation';

const loginSchema = z.object({
  username: z.email(),
  password: z.string().min(1),
});

const registerSchema = z
  .object({
    email: z.email(),
    password: z.string().min(PASSWORD_LENGTH.min).max(PASSWORD_LENGTH.max),
    passwordConfirm: z.string(),
  })
  .refine((data) => data.password === data.passwordConfirm, {
    message: "Passwords don't match",
    path: ['passwordConfirm'],
  });

export { loginSchema, registerSchema };
export type ILogin = z.infer<typeof loginSchema>;
export type IRegister = z.infer<typeof registerSchema>;
