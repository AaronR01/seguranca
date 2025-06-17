import express from &#39;express&#39;;
import { OAuth2Client } from &#39;google-auth-library&#39;;
import dotenv from &#39;dotenv&#39;;
dotenv.config();
const app = express();
const PORT = 3000;
const client = new OAuth2Client(
process.env.GOOGLE_CLIENT_ID,
process.env.GOOGLE_CLIENT_SECRET,
process.env.GOOGLE_REDIRECT_URI
);
app.get(&#39;/&#39;, (req, res) =&gt; {
const url = client.generateAuthUrl({
access_type: &#39;offline&#39;,
scope: [&#39;email&#39;, &#39;profile&#39;, &#39;openid&#39;],
});
res.send(`&lt;a href=&quot;${url}&quot;&gt;Login com Google&lt;/a&gt;`);
});
app.get(&#39;/callback&#39;, async (req, res) =&gt; {
try {
const { code } = req.query;
const { tokens } = await client.getToken(code);
client.setCredentials(tokens);
const ticket = await client.verifyIdToken({
idToken: tokens.id_token,
audience: process.env.GOOGLE_CLIENT_ID,
});
const payload = ticket.getPayload();
const name = encodeURIComponent(payload.name);
const email = encodeURIComponent(payload.email);
// Redireciona para a página de boas-vindas com parâmetros
res.redirect(`/welcome?name=${name}&amp;email=${email}`);
} catch (error) {
console.error(&#39;Erro na autenticação:&#39;, error);
res.status(500).send(&#39;Erro ao autenticar com o Google.&#39;);
}
});
app.get(&#39;/welcome&#39;, (req, res) =&gt; {
const { name, email } = req.query;
res.send(`
&lt;h1&gt;Bem-vindo, ${name}!&lt;/h1&gt;
&lt;p&gt;Seu e-mail: ${email}&lt;/p&gt;
`);
});
app.listen(PORT, () =&gt; {
console.log(`Servidor rodando em http://localhost:${PORT}`);
});
