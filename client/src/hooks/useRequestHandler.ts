import { customToaster } from '~/components/ui/toaster';

type HookType<T> = {
  f: (data: T) => any;
  successMsg?: string;
  successF?: () => void;
};

const useRequestHandler = <T>({ f, successMsg, successF }: HookType<T>) => {
  const handler = async (data: T) => {
    try {
      await f(data).unwrap();
      successMsg &&
        customToaster({
          description: successMsg,
          type: 'success',
        });
      successF && successF();
    } catch (error: any) {
      customToaster({
        description: error.data.detail,
        type: 'error',
      });
    }
  };

  return { handler };
};

export default useRequestHandler;
