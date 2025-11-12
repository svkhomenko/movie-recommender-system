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

const sendPasswordConfirmationSchema = z.object({
  email: z.email(),
});

const resetPasswordSchema = z
  .object({
    password: z.string().min(PASSWORD_LENGTH.min).max(PASSWORD_LENGTH.max),
    passwordConfirm: z.string(),
  })
  .refine((data) => data.password === data.passwordConfirm, {
    message: "Passwords don't match",
    path: ['passwordConfirm'],
  });

export { loginSchema, registerSchema, sendPasswordConfirmationSchema, resetPasswordSchema };
export type ILogin = z.infer<typeof loginSchema>;
export type IRegister = z.infer<typeof registerSchema>;
export type ISendPasswordConfirmation = z.infer<typeof sendPasswordConfirmationSchema>;
export type IResetPassword = z.infer<typeof resetPasswordSchema>;
