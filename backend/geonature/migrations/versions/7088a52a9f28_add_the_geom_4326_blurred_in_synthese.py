"""add the_geom_4326_blurred in synthese

Revision ID: 7088a52a9f28
Revises: 5a2c9c65129f
Create Date: 2023-10-13 21:30:43.239124

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "7088a52a9f28"
down_revision = "5a2c9c65129f"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        ALTER TABLE gn_synthese.synthese
        ADD COLUMN the_geom_4326_blurred geometry(geometry, 4326);
        """
    )

    op.execute(
        """
        UPDATE
            gn_synthese.synthese
        SET
	        the_geom_4326_blurred = st_transform(ref_geo.l_areas.geom, 4326) 
        FROM
                gn_synthese.cor_area_synthese AS cor_area_synthese_1
            JOIN ref_geo.l_areas ON
                cor_area_synthese_1.id_area = ref_geo.l_areas.id_area
            JOIN ref_geo.bib_areas_types ON
                ref_geo.l_areas.id_type = ref_geo.bib_areas_types.id_type
            JOIN gn_sensitivity.cor_sensitivity_area_type ON
                ref_geo.bib_areas_types.id_type = gn_sensitivity.cor_sensitivity_area_type.id_area_type
            WHERE
                cor_area_synthese_1.id_synthese = gn_synthese.synthese.id_synthese
                AND gn_sensitivity.cor_sensitivity_area_type.id_nomenclature_sensitivity = gn_synthese.synthese.id_nomenclature_sensitivity
                AND gn_synthese.synthese.id_nomenclature_sensitivity != (
                    SELECT 
                        id_nomenclature
                    FROM 
                        ref_nomenclatures.t_nomenclatures 
                    WHERE 
                        id_type = 16 
                        AND 
                        mnemonique = '0'
                    )
                AND gn_synthese.synthese.id_nomenclature_sensitivity != (
                    SELECT 
                        id_nomenclature
                    FROM 
                        ref_nomenclatures.t_nomenclatures 
                    WHERE 
                        id_type = 16 
                        AND 
                        mnemonique = '4'
                    )
        ; 
        """
    )


def downgrade():
    op.execute(
        """
        ALTER TABLE gn_synthese.synthese
        DROP COLUMN the_geom_4326_blurred;
        """
    )
