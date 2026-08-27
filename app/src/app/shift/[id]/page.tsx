import { ShiftView } from "@/components/ShiftView";
import { getShift } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function ShiftPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const shift = await getShift(id);
  return <ShiftView initial={shift} />;
}
