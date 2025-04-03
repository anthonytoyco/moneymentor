import { BreadcrumbHeader } from "@/components/breadcrumb-header";

export default async function Page() {
  return (
    <>
      <BreadcrumbHeader currentPage="Dashboard" />
      <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
        <p>Dashboard</p>
      </div>
    </>
  );
}
