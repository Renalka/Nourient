import re

with open('src/app/scanner/page.tsx', 'r') as f:
    content = f.read()

# Fix 1: Remove the auth redirect block
auth_redirect_block = """  useEffect(() => {
    if (!loading && !user) {
      router.push("/auth");
    }
  }, [user, loading, router]);"""
content = content.replace(auth_redirect_block, "")

# Fix 2: Remove !user check
content = content.replace("if (loading || !user) return null;", "if (loading) return null;")

# Fix 3: Fix ESLint unescaped entities
content = content.replace("Nourient's Recommendation", "Nourient&apos;s Recommendation")
content = content.replace("\"Deceptive\"", "&quot;Deceptive&quot;")
content = content.replace("Try a scan now — it's free", "Try a scan now — it&apos;s free")

with open('src/app/scanner/page.tsx', 'w') as f:
    f.write(content)
