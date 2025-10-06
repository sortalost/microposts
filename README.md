# qmaury-site
> qmaury's art site

## Deploy your own
1. Create a [vercel](https://vercel.com/signup) account,
2. [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/sortalost/qmaury-site),
3. Get a github [token](https://github.com/settings/tokens),
4. Add the github token to your environment variables, `settings -> environment-variables`,
5. Add your own `USERNAME`, `PASSWORD` and `SECRET_KEY` to the environment variables too,
5. Create another github repo for your image storage,
6. Populate `config.py` and add the other repo's name,
It should work then.

## Todo
- Editing and deleting posts. Right now they can be done manually by going to the second repository's `images.json`
- Exact time must be saved instead of 00:00 of that day.
