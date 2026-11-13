export default function PortalLayout({ children }: { children: React.ReactNode }) {
    return <div className="flex min-h-screen w-full flex-col bg-background">{children}</div>;
}